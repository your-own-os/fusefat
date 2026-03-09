import os
import subprocess


class TestMaxFilenameLength:
    """Test class for test_max_filename_length"""

    def test_max_filename_length(self, fat_image):
        """Handle maximum filename length."""
        image_path, mount = fat_image
        long_name = "a" * 255
        path = os.path.join(mount, long_name)
        try:
            with open(path, "w") as f:
                f.write("test")
            assert os.path.exists(path)
        except OSError:
            pass

    def test_max_filename_length_cli(self, fat_image):
        """Handle maximum filename length using CLI."""
        image_path, mount = fat_image
        long_name = "a" * 255
        path = os.path.join(mount, long_name)
        result = subprocess.run(
            ["sh", "-c", f"echo 'test' > '{path}'"], capture_output=True
        )
        if result.returncode == 0:
            assert os.path.exists(path)
