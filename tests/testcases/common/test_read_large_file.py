import os
import subprocess


class TestReadLargeFile:
    """Test class for test_read_large_file"""

    def test_read_large_file(self, fat_image):
        """Read large file."""
        image_path, mount = fat_image
        path = os.path.join(mount, "large.txt")
        content = "x" * (1024 * 1024)
        with open(path, "w") as f:
            f.write(content)
        with open(path, "r") as f:
            assert len(f.read()) == 1024 * 1024

    def test_read_large_file_cli(self, fat_image):
        """Read large file using CLI."""
        image_path, mount = fat_image
        path = os.path.join(mount, "large.txt")
        subprocess.run(
            ["dd", "if=/dev/zero", "of=" + path, "bs=1M", "count=1"], check=True
        )
        result = subprocess.run(
            ["wc", "-c", path], capture_output=True, text=True, check=True
        )
        assert result.stdout.strip().split()[0] == "1048576"
