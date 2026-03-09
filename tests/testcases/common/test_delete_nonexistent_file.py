import os
import pytest
import subprocess


class TestDeleteNonexistentFile:
    """Test class for test_delete_nonexistent_file"""

    def test_delete_nonexistent_file(self, fat_image):
        """Delete nonexistent file."""
        image_path, mount = fat_image
        path = os.path.join(mount, "nonexistent.txt")
        with pytest.raises(FileNotFoundError):
            os.remove(path)

    def test_delete_nonexistent_file_cli(self, fat_image):
        """Delete nonexistent file using CLI."""
        image_path, mount = fat_image
        path = os.path.join(mount, "nonexistent.txt")
        result = subprocess.run(["rm", path], capture_output=True)
        assert result.returncode != 0
