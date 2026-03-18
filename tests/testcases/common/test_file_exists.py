import os
import subprocess


class TestFileExists:
    """Test class for test_file_exists"""

    def test_file_exists(self, fat_image):
        """Check file exists."""
        image_path, mount = fat_image
        path = os.path.join(mount, "exists.txt")
        assert not os.path.exists(path)
        with open(path, "w") as f:
            f.write("test")
        assert os.path.exists(path)

    def test_file_exists_cli(self, fat_image):
        """Check file exists using CLI."""
        image_path, mount = fat_image
        path = os.path.join(mount, "exists.txt")
        result = subprocess.run(["test", "-e", path], capture_output=True)
        assert result.returncode != 0
        subprocess.run(["sh", "-c", f"echo 'test' > '{path}'"], check=True)
        result = subprocess.run(["test", "-e", path], capture_output=True)
        assert result.returncode == 0
