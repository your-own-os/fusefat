import os
import pytest
import subprocess


class TestDeleteNonexistentDirectory:
    """Test class for test_delete_nonexistent_directory"""

    def test_delete_nonexistent_directory(self, fat_image):
        """Delete nonexistent directory."""
        image_path, mount = fat_image
        path = os.path.join(mount, "nonexistent")
        with pytest.raises(FileNotFoundError):
            os.rmdir(path)

    def test_delete_nonexistent_directory_cli(self, fat_image):
        """Delete nonexistent directory using CLI."""
        image_path, mount = fat_image
        path = os.path.join(mount, "nonexistent")
        result = subprocess.run(["rmdir", path], capture_output=True)
        assert result.returncode != 0
