import os
import subprocess


class TestCreateDirectory:
    """Test class for test_create_directory"""

    def test_create_directory(self, fat_image):
        """Create directory."""
        image_path, mount = fat_image
        path = os.path.join(mount, "test_dir")
        os.mkdir(path)
        assert os.path.isdir(path)

    def test_create_directory_cli(self, fat_image):
        """Create directory using CLI."""
        image_path, mount = fat_image
        path = os.path.join(mount, "test_dir")
        subprocess.run(["mkdir", path], check=True)
        assert os.path.isdir(path)
