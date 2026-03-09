import os
import subprocess


class TestSeekBeginning:
    """Test class for test_seek_beginning"""

    def test_seek_beginning(self, fat_image):
        """Seek to beginning of file."""
        image_path, mount = fat_image
        path = os.path.join(mount, "seek_test.txt")
        with open(path, "w") as f:
            f.write("0123456789")
        with open(path, "r") as f:
            f.seek(0)
            assert f.read(1) == "0"

    def test_seek_beginning_cli(self, fat_image):
        """Seek to beginning of file using CLI."""
        image_path, mount = fat_image
        path = os.path.join(mount, "seek_test.txt")
        subprocess.run(["sh", "-c", f"echo -n '0123456789' > '{path}'"], check=True)
        result = subprocess.run(
            ["dd", "if=" + path, "bs=1", "count=1", "skip=0"],
            capture_output=True,
            text=True,
            check=True,
        )
        assert result.stdout.strip() == "0"
