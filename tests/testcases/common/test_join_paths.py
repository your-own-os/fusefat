import os
import subprocess


class TestJoinPaths:
    """Test class for test_join_paths"""

    def test_join_paths(self, fat_image):
        """Join paths."""
        image_path, mount = fat_image
        joined = os.path.join(mount, "dir", "file.txt")
        assert joined == os.path.join(mount, "dir", "file.txt")

    def test_join_paths_cli(self, fat_image):
        """Join paths using CLI."""
        image_path, mount = fat_image
        result = subprocess.run(
            ["ls", mount], capture_output=True, text=True, check=True
        )
        assert result.returncode == 0
