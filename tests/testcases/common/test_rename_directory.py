import os
import subprocess


class TestRenameDirectory:
    """Test class for test_rename_directory"""

    def test_rename_directory(self, fat_image):
        """Rename a directory."""
        image_path, mount = fat_image
        old_path = os.path.join(mount, "old_dir")
        new_path = os.path.join(mount, "new_dir")
        os.mkdir(old_path)
        os.rename(old_path, new_path)
        assert not os.path.exists(old_path)
        assert os.path.exists(new_path)

    def test_rename_directory_cli(self, fat_image):
        """Rename a directory using CLI."""
        image_path, mount = fat_image
        old_path = os.path.join(mount, "old_dir")
        new_path = os.path.join(mount, "new_dir")
        subprocess.run(["mkdir", old_path], check=True)
        subprocess.run(["mv", old_path, new_path], check=True)
        assert not os.path.exists(old_path)
        assert os.path.exists(new_path)
