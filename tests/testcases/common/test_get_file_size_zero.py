import os
import subprocess


class TestGetFileSizeZero:
    """Test class for test_get_file_size_zero"""

    def test_get_file_size_zero(self, fat_image):
        """Get size of empty file."""
        image_path, mount = fat_image
        path = os.path.join(mount, "empty.txt")
        with open(path, "w") as f:
            pass
        assert os.path.getsize(path) == 0, f"size: {os.path.getsize(path)}"

    def test_get_file_size_zero_cli(self, fat_image):
        """Get size of empty file using CLI."""
        image_path, mount = fat_image
        path = os.path.join(mount, "empty.txt")
        subprocess.run(["touch", path], check=True)
        result = subprocess.run(
            ["stat", "-c", "%s", path], capture_output=True, text=True, check=True
        )
        assert result.stdout.strip() == "0"
