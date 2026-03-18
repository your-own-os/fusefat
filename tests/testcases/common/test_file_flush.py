import os
import subprocess


class TestFileFlush:
    """Test class for test_file_flush"""

    def test_file_flush(self, fat_image):
        """Flush file buffers."""
        image_path, mount = fat_image
        path = os.path.join(mount, "flush_test.txt")
        with open(path, "w") as f:
            f.write("test")
            f.flush()
        with open(path, "r") as f:
            assert f.read() == "test"

    def test_file_flush_cli(self, fat_image):
        """Flush file buffers using CLI."""
        image_path, mount = fat_image
        path = os.path.join(mount, "flush_test.txt")
        subprocess.run(["sh", "-c", f"echo 'test' > '{path}'"], check=True)
        result = subprocess.run(
            ["cat", path], capture_output=True, text=True, check=True
        )
        assert result.stdout.strip() == "test"
