import os
import subprocess


class TestCreateEmptyFile:
    """Test class for test_create_empty_file"""

    def test_create_empty_file(self, fat_image):
        """Create empty file."""
        image_path, mount = fat_image
        path = os.path.join(mount, "empty.txt")
        with open(path, "w") as f:
            pass
        assert os.path.exists(path)
        assert os.path.getsize(path) == 0, f"size: {os.path.getsize(path)}"

    def test_create_empty_file_cli(self, fat_image):
        """Create empty file using CLI."""
        image_path, mount = fat_image
        path = os.path.join(mount, "empty.txt")
        subprocess.run(["touch", path], check=True)
        assert os.path.exists(path)
        assert os.path.getsize(path) == 0, f"size: {os.path.getsize(path)}"
