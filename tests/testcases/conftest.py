"""Test case fixtures - each test creates its own FAT image.

Usage:
    # Use debug backend (default)
    python -m pytest tests/ -v

    # Use kernel vfat backend
    python -m pytest tests/ -v --backend=kernel

    # Use production FUSE implementation
    python -m pytest tests/ -v --backend=production

    # Use release build
    python -m pytest tests/ -v --backend=release
"""

import os
import shutil
import subprocess
import sys
import tempfile
import time
from typing import BinaryIO, Generator, Optional, Tuple

import pytest


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MKIMAGES = os.path.join(SCRIPT_DIR, "..", "mkimages")
PROJECT_ROOT = os.path.join(SCRIPT_DIR, "..", "..")
FUSEFAT_DEBUG = os.path.join(PROJECT_ROOT, "target/debug/fusefat")
FUSEFAT_RELEASE = os.path.join(PROJECT_ROOT, "target/release/fusefat")


def pytest_addoption(parser):
    """Add --backend command line option."""
    parser.addoption(
        "--backend",
        action="store",
        default="debug",
        choices=["kernel", "production", "debug", "release"],
        help="Backend to use: kernel, production, debug, or release",
    )


def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line("markers", "kernel: tests for kernel vfat backend")
    config.addinivalue_line("markers", "production: tests for production FUSE backend")
    config.addinivalue_line("markers", "debug: tests for debug FUSE backend")
    config.addinivalue_line("markers", "release: tests for release FUSE backend")


# ============================================================================
# Helper functions
# ============================================================================


def get_fat_types_for_path(request):
    fspath = request.fspath
    if fspath:
        path = str(fspath)
        if "/fat12/" in path or path.endswith("fat12"):
            return ["fat12"]
        elif "/fat16/" in path or path.endswith("fat16"):
            return ["fat16"]
        elif "/fat32/" in path or path.endswith("fat32"):
            return ["fat32"]
    return ["fat12", "fat16", "fat32"]


def create_fat_image_file(temp_dir: str, fat_type: str) -> str:
    """Create a FAT filesystem image in the temp directory and return its path."""
    image_path = os.path.join(temp_dir, f"{fat_type}.img")
    if os.path.exists(image_path):
        os.remove(image_path)

    subprocess.run(
        [sys.executable, MKIMAGES, "--dir", temp_dir, "--fat-type", fat_type],
        check=True,
        capture_output=True,
    )

    return image_path


def create_test_workspace(temp_dir: str, fat_type: str) -> Tuple[str, str]:
    workspace = tempfile.mkdtemp(prefix=f"{fat_type}_", dir=temp_dir)
    mount_point = os.path.join(workspace, "mnt")
    os.mkdir(mount_point)
    return workspace, mount_point


# ============================================================================
# Kernel vfat backend (loop device mounting)
# ============================================================================


def create_image_and_mount_kernel(fat_type: str, temp_dir: str) -> Tuple[str, str, None, None]:
    """Create a FAT filesystem image and mount using kernel vfat."""
    workspace, mount_point = create_test_workspace(temp_dir, fat_type)
    image_path = create_fat_image_file(workspace, fat_type)

    fd, copy_path = tempfile.mkstemp(suffix=".img")
    os.close(fd)
    shutil.copy(image_path, copy_path)

    # Set up loop device as root
    result = subprocess.run(
        ["su", "-c", "losetup -f", "root"], capture_output=True, text=True
    )
    loop_dev = result.stdout.strip()

    subprocess.run(["su", "-c", f"losetup {loop_dev} {copy_path}", "root"], check=True)

    uid = os.getuid()
    gid = os.getgid()

    # Mount with current user permissions
    subprocess.run(
        [
            "su",
            "-c",
            f"mount -o uid={uid},gid={gid},umask=022 {loop_dev} {mount_point}",
            "root",
        ],
        check=True,
    )

    return copy_path, mount_point, None, None


def unmount_image_and_cleanup_kernel(image_path: str, mount_point: str, _proc: None = None, _log_file: None = None) -> None:
    subprocess.run(["su", "-c", f"umount {mount_point}", "root"], check=False)

    # detach loop device
    result = subprocess.run(
        ["su", "-c", f"losetup -j {image_path}", "root"], capture_output=True, text=True
    )
    if result.returncode == 0 and result.stdout:
        parts = result.stdout.split(":")
        if parts:
            dev = parts[0]
            subprocess.run(["su", "-c", f"losetup -d {dev}", "root"], check=False)

    os.rmdir(mount_point)
    os.remove(image_path)


# ============================================================================
# FUSE backend (using fusefat binary)
# ============================================================================


def create_image_and_mount_fuse(fat_type: str, binary: str, temp_dir: str, debug: bool = False) -> Tuple[str, str, subprocess.Popen[bytes], BinaryIO]:
    """Create a FAT filesystem image and mount using fusefat."""
    workspace, mount_point = create_test_workspace(temp_dir, fat_type)
    image_path = create_fat_image_file(workspace, fat_type)
    log_file = open(os.path.join(workspace, "fusefat.log"), "wb")

    cmd = [binary]
    if debug:
        cmd.extend(["-d", "-f"])
    cmd.extend([image_path, mount_point])

    proc = subprocess.Popen(cmd, stdout=log_file, stderr=subprocess.STDOUT)

    deadline = time.time() + 5
    while time.time() < deadline:
        if proc.poll() is not None:
            proc.wait(timeout=2)
            log_file.flush()
            with open(log_file.name, "r", encoding="utf-8", errors="replace") as f:
                raise RuntimeError(f"fusefat failed to start: {f.read()}")

        result = subprocess.run(
            ["mountpoint", "-q", mount_point],
            check=False,
            capture_output=True,
        )
        if result.returncode == 0:
            return image_path, mount_point, proc, log_file

        time.sleep(0.1)

    proc.terminate()
    try:
        proc.wait(timeout=2)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait(timeout=2)

    log_file.flush()
    with open(log_file.name, "r", encoding="utf-8", errors="replace") as f:
        details = f.read()

    raise RuntimeError(f"fusefat mount timed out for {mount_point}: {details}")


def unmount_image_and_cleanup_fuse(image_path: str, mount_point: str, proc: Optional[subprocess.Popen[bytes]] = None, log_file: Optional[BinaryIO] = None) -> None:
    try:
        subprocess.run(["fusermount", "-u", mount_point], check=False, timeout=5)
    except subprocess.TimeoutExpired:
        subprocess.run(["fusermount", "-uz", mount_point], check=False, timeout=5)
    if proc is not None:
        try:
            proc.wait(timeout=2)
        except subprocess.TimeoutExpired:
            proc.terminate()
            try:
                proc.wait(timeout=2)
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.wait(timeout=2)
    if log_file is not None and not log_file.closed:
        log_file.close()
    shutil.rmtree(os.path.dirname(mount_point), ignore_errors=True)


# ============================================================================
# Fixtures
# ============================================================================


@pytest.fixture(scope="session")
def temp_dir():
    # create a single temp directory for all test images
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture(params=["fat12", "fat16", "fat32"])
def fat_image(request, pytestconfig, temp_dir) -> Generator[Tuple[str, str], None, None]:
    backends = {
        "production": (
            lambda ft: create_image_and_mount_fuse(ft, "fusefat", temp_dir),
            unmount_image_and_cleanup_fuse,
        ),
        "debug": (
            lambda ft: create_image_and_mount_fuse(
                ft, FUSEFAT_DEBUG, temp_dir, debug=True
            ),
            unmount_image_and_cleanup_fuse,
        ),
        "release": (
            lambda ft: create_image_and_mount_fuse(ft, FUSEFAT_RELEASE, temp_dir),
            unmount_image_and_cleanup_fuse,
        ),
        "kernel": (
            lambda ft: create_image_and_mount_kernel(ft, temp_dir),
            unmount_image_and_cleanup_kernel,
        ),
    }

    fat_type = request.param
    if fat_type not in get_fat_types_for_path(request):
        pytest.skip(f"Test not applicable for {fat_type}")

    backend = pytestconfig.getoption("--backend")
    create_fn, unmount_fn = backends[backend]

    image_path, mount_point, proc, log_file = create_fn(fat_type)
    yield image_path, mount_point
    unmount_fn(image_path, mount_point, proc, log_file)
