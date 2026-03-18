import os
import subprocess


class TestOverwriteFile:
    """Test class for test_overwrite_file"""

    def test_overwrite_file(self, fat_image):
        """Overwrite file content."""
        image_path, mount = fat_image
        path = os.path.join(mount, "overwrite.txt")
        with open(path, "w") as f:
            f.write("original")
        with open(path, "w") as f:
            f.write("new content")
        with open(path, "r") as f:
            assert f.read() == "new content"

    def test_overwrite_file_cli(self, fat_image):
        """Overwrite file content using CLI."""
        image_path, mount = fat_image
        path = os.path.join(mount, "overwrite.txt")
        subprocess.run(["sh", "-c", f"echo 'original' > '{path}'"], check=True)
        subprocess.run(["sh", "-c", f"echo 'new content' > '{path}'"], check=True)
        result = subprocess.run(
            ["cat", path], capture_output=True, text=True, check=True
        )
        assert result.stdout.strip() == "new content"
