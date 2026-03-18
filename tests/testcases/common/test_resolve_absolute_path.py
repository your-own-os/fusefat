import os
import subprocess


class TestResolveAbsolutePath:
    """Test class for test_resolve_absolute_path"""

    def test_resolve_absolute_path(self, fat_image):
        """Resolve absolute path."""
        image_path, mount = fat_image
        path = os.path.join(mount, "test.txt")
        resolved = os.path.realpath(path)
        assert os.path.isabs(resolved)

    def test_resolve_absolute_path_cli(self, fat_image):
        """Resolve absolute path using CLI."""
        image_path, mount = fat_image
        path = os.path.join(mount, "test.txt")
        result = subprocess.run(
            ["readlink", "-f", path], capture_output=True, text=True, check=True
        )
        assert os.path.isabs(result.stdout.strip())
