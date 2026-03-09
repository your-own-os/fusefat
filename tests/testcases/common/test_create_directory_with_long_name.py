import os
import subprocess


class TestCreateDirectoryWithLongName:
    """Test class for test_create_directory_with_long_name"""

    def test_create_directory_with_long_name(self, fat_image):
        """Create directory with long name."""
        image_path, mount = fat_image
        long_name = "a" * 200
        path = os.path.join(mount, long_name)
        os.mkdir(path)
        assert os.path.isdir(path)

    def test_create_directory_with_long_name_cli(self, fat_image):
        """Create directory with long name using CLI."""
        image_path, mount = fat_image
        long_name = "a" * 200
        path = os.path.join(mount, long_name)
        subprocess.run(["mkdir", path], check=True)
        assert os.path.isdir(path)
