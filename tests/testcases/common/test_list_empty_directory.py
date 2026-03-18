import os
import subprocess


class TestListEmptyDirectory:
    """Test class for test_list_empty_directory"""

    def test_list_empty_directory(self, fat_image):
        """List empty directory."""
        image_path, mount = fat_image
        entries = os.listdir(mount)
        assert len(entries) == 0

    def test_list_empty_directory_cli(self, fat_image):
        """List empty directory using CLI."""
        image_path, mount = fat_image
        result = subprocess.run(
            ["ls", mount], capture_output=True, text=True, check=True
        )
        assert len(result.stdout.strip()) == 0
