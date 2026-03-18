import os
import subprocess


class TestReadWriteText:
    """Test class for test_read_write_text"""

    def test_read_write_text(self, fat_image):
        """Read and write text content."""
        image_path, mount = fat_image
        path = os.path.join(mount, "test.txt")
        content = "Hello, FAT filesystem!"
        with open(path, "w") as f:
            f.write(content)
        with open(path, "r") as f:
            assert f.read() == content

    def test_read_write_text_cli(self, fat_image):
        """Read and write text content using CLI."""
        image_path, mount = fat_image
        path = os.path.join(mount, "test.txt")
        content = "Hello, FAT filesystem!"
        subprocess.run(["sh", "-c", f"echo '{content}' > '{path}'"], check=True)
        result = subprocess.run(
            ["cat", path], capture_output=True, text=True, check=True
        )
        assert result.stdout == content + "\n"
