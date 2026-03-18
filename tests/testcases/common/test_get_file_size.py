import os
import subprocess


class TestGetFileSize:
    """Test class for test_get_file_size"""

    def test_get_file_size(self, fat_image):
        """Get file size."""
        image_path, mount = fat_image
        path = os.path.join(mount, "size_test.txt")
        content = "x" * 1000
        with open(path, "w") as f:
            f.write(content)
        assert os.path.getsize(path) == 1000, f"size: {os.path.getsize(path)}"

    def test_get_file_size_cli(self, fat_image):
        """Get file size using CLI."""
        image_path, mount = fat_image
        path = os.path.join(mount, "size_test.txt")
        subprocess.run(
            ["sh", "-c", f"printf 'x%.0s' {{1..1000}} > '{path}'"], check=True
        )
        result = subprocess.run(
            ["stat", "-c", "%s", path], capture_output=True, text=True, check=True
        )
        assert result.stdout.strip() == "1000"
