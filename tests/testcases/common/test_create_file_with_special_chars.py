import os
import subprocess


class TestCreateFileWithSpecialChars:
    """Test class for test_create_file_with_special_chars"""

    def test_create_file_with_special_chars(self, fat_image):
        """Create file with special characters in name."""
        image_path, mount = fat_image
        special_names = ["file.txt", "file.test.txt", "file.with.dots.txt"]
        for name in special_names:
            path = os.path.join(mount, name)
            with open(path, "w") as f:
                f.write("test")
            assert os.path.exists(path)

    def test_create_file_with_special_chars_cli(self, fat_image):
        """Create file with special characters in name using CLI."""
        image_path, mount = fat_image
        special_names = ["file.txt", "file.test.txt", "file.with.dots.txt"]
        for name in special_names:
            path = os.path.join(mount, name)
            subprocess.run(["sh", "-c", f"echo 'test' > '{path}'"], check=True)
            assert os.path.exists(path)
