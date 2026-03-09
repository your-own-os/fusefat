import os
import subprocess


class TestSplitPath:
    """Test class for test_split_path"""

    def test_split_path(self, fat_image):
        """Split path."""
        path = "/mount/dir/file.txt"
        dirname, basename = os.path.split(path)
        assert dirname == "/mount/dir"
        assert basename == "file.txt"

    def test_split_path_cli(self, fat_image):
        """Split path using CLI."""
        image_path, mount = fat_image
        result = subprocess.run(
            ["dirname", "/mount/dir/file.txt"],
            capture_output=True,
            text=True,
            check=True,
        )
        assert result.stdout.strip() == "/mount/dir"
        result = subprocess.run(
            ["basename", "/mount/dir/file.txt"],
            capture_output=True,
            text=True,
            check=True,
        )
        assert result.stdout.strip() == "file.txt"
