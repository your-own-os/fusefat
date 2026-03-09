import os
import subprocess


class TestFilenameWithUnicode:
    """Test class for test_filename_with_unicode"""

    def test_filename_with_unicode(self, fat_image):
        """Handle filename with unicode."""
        image_path, mount = fat_image
        path = os.path.join(mount, "文件.txt")
        with open(path, "w") as f:
            f.write("test")
        assert os.path.exists(path)

    def test_filename_with_unicode_cli(self, fat_image):
        """Handle filename with unicode using CLI."""
        image_path, mount = fat_image
        path = os.path.join(mount, "文件.txt")
        subprocess.run(["sh", "-c", f"echo 'test' > '{path}'"], check=True)
        assert os.path.exists(path)
