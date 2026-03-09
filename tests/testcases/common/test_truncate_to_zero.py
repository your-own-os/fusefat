import os
import subprocess


class TestTruncateToZero:
    """Test class for test_truncate_to_zero"""

    def test_truncate_to_zero(self, fat_image):
        """Truncate file to zero."""
        image_path, mount = fat_image
        path = os.path.join(mount, "trunc_zero.txt")
        with open(path, "w") as f:
            f.write("x" * 1000)
        with open(path, "w") as f:
            f.truncate(0)
        assert os.path.getsize(path) == 0, f"size: {os.path.getsize(path)}"

    def test_truncate_to_zero_cli(self, fat_image):
        """Truncate file to zero using CLI."""
        image_path, mount = fat_image
        path = os.path.join(mount, "trunc_zero.txt")
        subprocess.run(
            ["sh", "-c", f"printf 'x%.0s' {{1..1000}} > '{path}'"], check=True
        )
        subprocess.run(["truncate", "-s", "0", path], check=True)
        assert os.path.getsize(path) == 0
