import os
import subprocess


class TestMultipleReaders:
    """Test class for test_multiple_readers"""

    def test_multiple_readers(self, fat_image):
        """Multiple processes reading same file."""
        image_path, mount = fat_image
        path = os.path.join(mount, "multi_read.txt")
        with open(path, "w") as f:
            f.write("shared content")
        for _ in range(5):
            with open(path, "r") as f:
                assert f.read() == "shared content"

    def test_multiple_readers_cli(self, fat_image):
        """Multiple processes reading same file using CLI."""
        image_path, mount = fat_image
        path = os.path.join(mount, "multi_read.txt")
        subprocess.run(["sh", "-c", f"echo 'shared content' > '{path}'"], check=True)
        for _ in range(5):
            result = subprocess.run(
                ["cat", path], capture_output=True, text=True, check=True
            )
            assert result.stdout.strip() == "shared content"
