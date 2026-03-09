import os
import subprocess


class TestTruncateFile:
    """Test class for test_truncate_file"""

    def test_truncate_file(self, fat_image):
        """Truncate file."""
        image_path, mount = fat_image
        path = os.path.join(mount, "truncate.txt")
        with open(path, "w") as f:
            f.write("x" * 1000)
        with open(path, "r+") as f:
            f.truncate(500)
        assert os.path.getsize(path) == 500, f"size: {os.path.getsize(path)}"

    def test_truncate_file_cli(self, fat_image):
        """Truncate file using CLI."""
        image_path, mount = fat_image
        path = os.path.join(mount, "truncate.txt")
        subprocess.run(
            ["sh", "-c", f"printf 'x%.0s' {{1..1000}} > '{path}'"], check=True
        )
        subprocess.run(["truncate", "-s", "500", path], check=True)
        result = subprocess.run(
            ["stat", "-c", "%s", path], capture_output=True, text=True, check=True
        )
        assert result.stdout.strip() == "500"
