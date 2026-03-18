import os
import subprocess


class TestSeekEnd:
    """Test class for test_seek_end"""

    def test_seek_end(self, fat_image):
        """Seek to end of file."""
        image_path, mount = fat_image
        path = os.path.join(mount, "seek_end.txt")
        with open(path, "w") as f:
            f.write("0123456789")
        with open(path, "r") as f:
            f.seek(0, 2)
            assert f.tell() == 10

    def test_seek_end_cli(self, fat_image):
        """Seek to end of file using CLI."""
        image_path, mount = fat_image
        path = os.path.join(mount, "seek_end.txt")
        subprocess.run(["sh", "-c", f"echo -n '0123456789' > '{path}'"], check=True)
        result = subprocess.run(
            ["wc", "-c", path], capture_output=True, text=True, check=True
        )
        assert result.stdout.strip().split()[0] == "10"
