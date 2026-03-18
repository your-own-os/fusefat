import os
import subprocess


class TestCreateMultipleDirectories:
    """Test class for test_create_multiple_directories"""

    def test_create_multiple_directories(self, fat_image):
        """Create multiple directories."""
        image_path, mount = fat_image
        for i in range(10):
            path = os.path.join(mount, f"dir_{i}")
            os.mkdir(path)
        for i in range(10):
            assert os.path.isdir(os.path.join(mount, f"dir_{i}"))

    def test_create_multiple_directories_cli(self, fat_image):
        """Create multiple directories using CLI."""
        image_path, mount = fat_image
        for i in range(10):
            path = os.path.join(mount, f"dir_{i}")
            subprocess.run(["mkdir", path], check=True)
        for i in range(10):
            assert os.path.isdir(os.path.join(mount, f"dir_{i}"))
