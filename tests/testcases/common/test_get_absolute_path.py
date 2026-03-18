import os
import subprocess


class TestGetAbsolutePath:
    """Test class for test_get_absolute_path"""

    def test_get_absolute_path(self, fat_image):
        """Get absolute path."""
        image_path, mount = fat_image
        rel_path = "file.txt"
        abs_path = os.path.abspath(rel_path)
        assert os.path.isabs(abs_path)

    def test_get_absolute_path_cli(self, fat_image):
        """Get absolute path using CLI."""
        image_path, mount = fat_image
        result = subprocess.run(
            ["readlink", "-f", "."], capture_output=True, text=True, cwd=mount
        )
        assert os.path.isabs(result.stdout.strip())
