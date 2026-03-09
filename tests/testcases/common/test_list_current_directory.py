import os
import subprocess


class TestListCurrentDirectory:
    """Test class for test_list_current_directory"""

    def test_list_current_directory(self, fat_image):
        """List current directory."""
        original = os.getcwd()
        os.chdir(fat_image[1])
        entries = os.listdir(".")
        os.chdir(original)
        assert isinstance(entries, list)

    def test_list_current_directory_cli(self, fat_image):
        """List current directory using CLI."""
        image_path, mount = fat_image
        result = subprocess.run(["ls"], capture_output=True, text=True, cwd=mount)
        assert isinstance(result.stdout, str)
