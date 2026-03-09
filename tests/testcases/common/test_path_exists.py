import os
import subprocess


class TestPathExists:
    """Test class for test_path_exists"""

    def test_path_exists(self, fat_image):
        """Check path exists."""
        image_path, mount = fat_image
        assert os.path.exists(mount)

    def test_path_exists_cli(self, fat_image):
        """Check path exists using CLI."""
        image_path, mount = fat_image
        result = subprocess.run(["test", "-e", mount], capture_output=True)
        assert result.returncode == 0
