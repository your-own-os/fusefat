import os
import subprocess


class TestDeleteFile:
    """Test class for test_delete_file"""

    def test_delete_file(self, fat_image):
        """Delete existing file."""
        image_path, mount = fat_image
        path = os.path.join(mount, "delete_me.txt")
        with open(path, "w") as f:
            f.write("to be deleted")
        assert os.path.exists(path)
        os.remove(path)
        assert not os.path.exists(path)

    def test_delete_file_cli(self, fat_image):
        """Delete existing file using CLI."""
        image_path, mount = fat_image
        path = os.path.join(mount, "delete_me.txt")
        subprocess.run(["sh", "-c", f"echo 'to be deleted' > '{path}'"], check=True)
        assert os.path.exists(path)
        subprocess.run(["rm", path], check=True)
        assert not os.path.exists(path)
