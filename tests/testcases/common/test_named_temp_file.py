import os
import tempfile
import subprocess


class TestNamedTempFile:
    """Test class for test_named_temp_file"""

    def test_named_temp_file(self, fat_image):
        """Create named temporary file."""
        image_path, mount = fat_image
        fd, path = tempfile.mkstemp(dir=mount)
        os.close(fd)
        assert os.path.exists(path)
        os.remove(path)

    def test_named_temp_file_cli(self, fat_image):
        """Create named temporary file using CLI."""
        image_path, mount = fat_image
        path = os.path.join(mount, "tempfile")
        subprocess.run(["mktemp", path + ".XXXXXX"], check=True, cwd=mount)
        result = subprocess.run(
            ["ls", mount], capture_output=True, text=True, check=True
        )
        assert "tempfile" in result.stdout
