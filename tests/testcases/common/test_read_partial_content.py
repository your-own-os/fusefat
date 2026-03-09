import os
import subprocess


class TestReadPartialContent:
    """Test class for test_read_partial_content"""

    def test_read_partial_content(self, fat_image):
        """Read partial file content."""
        image_path, mount = fat_image
        path = os.path.join(mount, "partial.txt")
        with open(path, "w") as f:
            f.write("0123456789")
        with open(path, "r") as f:
            assert f.read(5) == "01234"

    def test_read_partial_content_cli(self, fat_image):
        """Read partial file content using CLI."""
        image_path, mount = fat_image
        path = os.path.join(mount, "partial.txt")
        subprocess.run(["sh", "-c", f"echo -n '0123456789' > '{path}'"], check=True)
        result = subprocess.run(
            ["dd", "if=" + path, "bs=1", "count=5"],
            capture_output=True,
            text=True,
            check=True,
        )
        assert result.stdout.strip() == "01234"
