import os
import subprocess


class TestIsFile:
    """Test class for test_is_file"""

    def test_is_file(self, fat_image):
        """Check if path is file."""
        image_path, mount = fat_image
        file_path = os.path.join(mount, "file.txt")
        with open(file_path, "w") as f:
            f.write("test")
        assert os.path.isfile(file_path)

    def test_is_file_cli(self, fat_image):
        """Check if path is file using CLI."""
        image_path, mount = fat_image
        file_path = os.path.join(mount, "file.txt")
        subprocess.run(["sh", "-c", f"echo 'test' > '{file_path}'"], check=True)
        result = subprocess.run(["test", "-f", file_path], capture_output=True)
        assert result.returncode == 0
