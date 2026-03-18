import os
import subprocess


class TestSeekMiddle:
    """Test class for test_seek_middle"""

    def test_seek_middle(self, fat_image):
        """Seek to middle of file."""
        image_path, mount = fat_image
        path = os.path.join(mount, "seek_mid.txt")
        with open(path, "w") as f:
            f.write("0123456789")
        with open(path, "r") as f:
            f.seek(5)
            assert f.read(1) == "5"

    def test_seek_middle_cli(self, fat_image):
        """Seek to middle of file using CLI."""
        image_path, mount = fat_image
        path = os.path.join(mount, "seek_mid.txt")
        subprocess.run(["sh", "-c", f"echo -n '0123456789' > '{path}'"], check=True)
        result = subprocess.run(
            ["dd", "if=" + path, "bs=1", "count=1", "skip=5"],
            capture_output=True,
            text=True,
            check=True,
        )
        assert result.stdout.strip() == "5"
