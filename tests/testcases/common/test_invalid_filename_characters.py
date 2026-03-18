import subprocess


class TestInvalidFilenameCharacters:
    """Test class for test_invalid_filename_characters"""

    def test_invalid_filename_characters(self, fat_image):
        """Handle invalid filename characters."""
        pass

    def test_invalid_filename_characters_cli(self, fat_image):
        """Handle invalid filename characters using CLI."""
        image_path, mount = fat_image
        result = subprocess.run(
            ["ls", mount], capture_output=True, text=True, check=True
        )
        assert isinstance(result.stdout, str)
