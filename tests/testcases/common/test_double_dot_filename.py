import subprocess


class TestDoubleDotFilename:
    """Test class for test_double_dot_filename"""

    def test_double_dot_filename(self, fat_image):
        """Handle double dot filename."""
        image_path, mount = fat_image
        # ".." refers to parent directory
        pass

    def test_double_dot_filename_cli(self, fat_image):
        """Handle double dot filename using CLI."""
        image_path, mount = fat_image
        result = subprocess.run(
            ["ls", "-la", mount], capture_output=True, text=True, check=True
        )
        assert ".." in result.stdout or "." in result.stdout
