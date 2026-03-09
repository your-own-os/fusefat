import os
import subprocess


class TestRenameFile:
    """Test class for test_rename_file"""

    def test_rename_file(self, fat_image):
        """Rename a file."""
        image_path, mount = fat_image
        old_path = os.path.join(mount, "old_name.txt")
        new_path = os.path.join(mount, "new_name.txt")
        with open(old_path, "w") as f:
            f.write("test")
        os.rename(old_path, new_path)
        assert not os.path.exists(old_path)
        assert os.path.exists(new_path)

    def test_rename_file_cli(self, fat_image):
        """Rename a file using CLI."""
        image_path, mount = fat_image
        old_path = os.path.join(mount, "old_name.txt")
        new_path = os.path.join(mount, "new_name.txt")
        subprocess.run(["sh", "-c", f"echo 'test' > '{old_path}'"], check=True)
        subprocess.run(["mv", old_path, new_path], check=True)
        assert not os.path.exists(old_path)
        assert os.path.exists(new_path)
