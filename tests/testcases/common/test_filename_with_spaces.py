import os
import subprocess


class TestFilenameWithSpaces:
    """Test class for test_filename_with_spaces"""

    def test_filename_with_spaces(self, fat_image):
        """Handle filename with spaces."""
        image_path, mount = fat_image
        path = os.path.join(mount, "file with spaces.txt")
        with open(path, "w") as f:
            f.write("test")
        assert os.path.exists(path)

    def test_filename_with_spaces_cli(self, fat_image):
        """Handle filename with spaces using CLI."""
        image_path, mount = fat_image
        path = os.path.join(mount, "file with spaces.txt")
        subprocess.run(["sh", "-c", f"echo 'test' > '{path}'"], check=True)
        assert os.path.exists(path)
