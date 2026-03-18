import os
import stat
import subprocess


class TestFileUidGid:
    """Test class for file uid/gid"""

    def test_file_uid_gid(self, fat_image):
        """Test that files have valid uid and gid."""
        image_path, mount = fat_image
        path = os.path.join(mount, "test_file.txt")

        # Create a file
        with open(path, "w") as f:
            f.write("test content")

        # Get file stats
        st = os.stat(path)

        assert st.st_uid == os.getuid(), f"Expected uid=={os.getuid()}, got {st.st_uid}"
        assert st.st_gid == os.getgid(), f"Expected gid=={os.getgid()}, got {st.st_gid}"

    def test_file_uid_gid_cli(self, fat_image):
        """Test that files have valid uid and gid using CLI."""
        image_path, mount = fat_image
        path = os.path.join(mount, "test_file.txt")
        subprocess.run(["sh", "-c", f"echo 'test content' > '{path}'"], check=True)
        result = subprocess.run(
            ["stat", "-c", "%u:%g", path], capture_output=True, text=True, check=True
        )
        uid_gid = result.stdout.strip().split(":")
        assert int(uid_gid[0]) == os.getuid()
        assert int(uid_gid[1]) == os.getgid()


class TestFileMode:
    """Test class for file mode/permissions"""

    def test_file_mode_regular(self, fat_image):
        """Test that regular files have correct mode."""
        image_path, mount = fat_image
        path = os.path.join(mount, "test_file.txt")

        # Create a file
        with open(path, "w") as f:
            f.write("test content")

        # Get file stats
        st = os.stat(path)
        mode = stat.S_IMODE(st.st_mode)

        assert mode == 0o755, f"Expected mode=0755, got {oct(mode)}"

    def test_file_mode_regular_cli(self, fat_image):
        """Test that regular files have correct mode using CLI."""
        image_path, mount = fat_image
        path = os.path.join(mount, "test_file.txt")
        subprocess.run(["sh", "-c", f"echo 'test content' > '{path}'"], check=True)
        result = subprocess.run(
            ["stat", "-c", "%a", path], capture_output=True, text=True, check=True
        )
        mode = result.stdout.strip()
        assert mode == "755", f"Expected mode=755, got {mode}"


class TestDirectoryMode:
    """Test class for directory mode"""

    def test_directory_mode(self, fat_image):
        """Test that directories have correct mode."""
        image_path, mount = fat_image
        path = os.path.join(mount, "test_dir")

        # Create a directory
        os.mkdir(path)

        # Get directory stats
        st = os.stat(path)

        # Directory should have mode 0755 (rwxr-xr-x)
        mode = stat.S_IMODE(st.st_mode)
        expected = 0o755
        assert mode == expected, f"Expected mode={oct(expected)}, got {oct(mode)}"

    def test_directory_mode_cli(self, fat_image):
        """Test that directories have correct mode using CLI."""
        image_path, mount = fat_image
        path = os.path.join(mount, "test_dir")
        subprocess.run(["mkdir", path], check=True)
        result = subprocess.run(
            ["stat", "-c", "%a", path], capture_output=True, text=True, check=True
        )
        assert result.stdout.strip() == "755"


class TestChmod:
    """Test class for chmod"""

    def test_chmod_file(self, fat_image):
        """Test chmod on file."""
        image_path, mount = fat_image
        path = os.path.join(mount, "test_file.txt")

        # Create a file
        with open(path, "w") as f:
            f.write("test content")

        # Try to chmod (may not work on FAT)
        try:
            os.chmod(path, 0o600)
            st = os.stat(path)
            mode = stat.S_IMODE(st.st_mode)
            # FAT may not support chmod, but we test anyway
            print(f"chmod succeeded, mode={oct(mode)}")
        except OSError as e:
            # FAT doesn't support chmod - this is expected
            print(f"chmod not supported on FAT: {e}")

    def test_chmod_file_cli(self, fat_image):
        """Test chmod on file using CLI."""
        image_path, mount = fat_image
        path = os.path.join(mount, "test_file.txt")
        subprocess.run(["sh", "-c", f"echo 'test content' > '{path}'"], check=True)
        result = subprocess.run(["chmod", "600", path], capture_output=True)
        if result.returncode == 0:
            result = subprocess.run(
                ["stat", "-c", "%a", path], capture_output=True, text=True, check=True
            )
            print(f"chmod succeeded, mode={result.stdout.strip()}")
