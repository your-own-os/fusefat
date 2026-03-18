import os
import subprocess


class TestCreateFileWithLongName:
    """Test class for test_create_file_with_long_name"""

    def test_create_file_with_long_name(self, fat_image):
        """Create file with long name."""
        image_path, mount = fat_image
        long_name = "a" * 200 + ".txt"
        path = os.path.join(mount, long_name)
        with open(path, "w") as f:
            f.write("long name test")
        assert os.path.exists(path)

    def test_create_file_with_long_name_cli(self, fat_image):
        """Create file with long name using CLI."""
        image_path, mount = fat_image
        long_name = "a" * 200 + ".txt"
        path = os.path.join(mount, long_name)
        subprocess.run(["sh", "-c", f"echo 'long name test' > '{path}'"], check=True)
        assert os.path.exists(path)
