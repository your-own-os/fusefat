import os
import subprocess


class TestListDirectoryWithSubdirs:
    """Test class for test_list_directory_with_subdirs"""

    def test_list_directory_with_subdirs(self, fat_image):
        """List directory with subdirectories."""
        image_path, mount = fat_image
        for i in range(3):
            os.mkdir(os.path.join(mount, f"dir{i}"))
        for i in range(3):
            with open(os.path.join(mount, f"file{i}.txt"), "w") as f:
                f.write("test")
        entries = os.listdir(mount)
        for i in range(3):
            assert f"dir{i}" in entries
            assert f"file{i}.txt" in entries

    def test_list_directory_with_subdirs_cli(self, fat_image):
        """List directory with subdirectories using CLI."""
        image_path, mount = fat_image
        for i in range(3):
            subprocess.run(["mkdir", os.path.join(mount, f"dir{i}")], check=True)
        for i in range(3):
            subprocess.run(
                ["sh", "-c", f"echo 'test' > '{mount}/file{i}.txt'"], check=True
            )
        result = subprocess.run(
            ["ls", mount], capture_output=True, text=True, check=True
        )
        for i in range(3):
            assert f"dir{i}" in result.stdout
            assert f"file{i}.txt" in result.stdout
