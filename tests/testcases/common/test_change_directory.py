import os
import subprocess


class TestChangeDirectory:
    """Test class for test_change_directory"""

    def test_change_directory(self, fat_image):
        """Change working directory."""
        image_path, mount = fat_image
        original = os.getcwd()
        os.chdir(mount)
        assert os.getcwd() == mount
        os.chdir(original)

    def test_change_directory_cli(self, fat_image):
        """Change working directory using CLI."""
        image_path, mount = fat_image
        result = subprocess.run(
            ["pwd"], capture_output=True, text=True, cwd=mount, check=True
        )
        assert result.stdout.strip() == mount
