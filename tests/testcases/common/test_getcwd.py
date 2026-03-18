import os
import subprocess


class TestGetcwd:
    """Test class for test_getcwd"""

    def test_getcwd(self, fat_image):
        """Get current working directory."""
        original = os.getcwd()
        os.chdir(fat_image[1])
        cwd = os.getcwd()
        os.chdir(original)
        assert cwd == fat_image[1]

    def test_getcwd_cli(self, fat_image):
        """Get current working directory using CLI."""
        image_path, mount = fat_image
        result = subprocess.run(
            ["pwd"], capture_output=True, text=True, cwd=mount, check=True
        )
        assert result.stdout.strip() == mount
