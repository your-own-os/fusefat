import os
import subprocess


class TestIsDirectory:
    """Test class for test_is_directory"""

    def test_is_directory(self, fat_image):
        """Check if path is directory."""
        image_path, mount = fat_image
        dir_path = os.path.join(mount, "testdir")
        os.mkdir(dir_path)
        assert os.path.isdir(dir_path)

    def test_is_directory_cli(self, fat_image):
        """Check if path is directory using CLI."""
        image_path, mount = fat_image
        dir_path = os.path.join(mount, "testdir")
        subprocess.run(["mkdir", dir_path], check=True)
        result = subprocess.run(["test", "-d", dir_path], capture_output=True)
        assert result.returncode == 0
