import os
import subprocess


class TestCreateNestedDirectory:
    """Test class for test_create_nested_directory"""

    def test_create_nested_directory(self, fat_image):
        """Create nested directories."""
        image_path, mount = fat_image
        path = os.path.join(mount, "parent/child/grandchild")
        os.makedirs(path)
        assert os.path.isdir(path)

    def test_create_nested_directory_cli(self, fat_image):
        """Create nested directories using CLI."""
        image_path, mount = fat_image
        path = os.path.join(mount, "parent/child/grandchild")
        subprocess.run(["mkdir", "-p", path], check=True)
        assert os.path.isdir(path)
