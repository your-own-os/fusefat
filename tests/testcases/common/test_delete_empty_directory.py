import os
import subprocess


class TestDeleteEmptyDirectory:
    """Test class for test_delete_empty_directory"""

    def test_delete_empty_directory(self, fat_image):
        """Delete empty directory."""
        image_path, mount = fat_image
        path = os.path.join(mount, "empty_dir")
        os.mkdir(path)
        os.rmdir(path)
        assert not os.path.exists(path)

    def test_delete_empty_directory_cli(self, fat_image):
        """Delete empty directory using CLI."""
        image_path, mount = fat_image
        path = os.path.join(mount, "empty_dir")
        subprocess.run(["mkdir", path], check=True)
        subprocess.run(["rmdir", path], check=True)
        assert not os.path.exists(path)
