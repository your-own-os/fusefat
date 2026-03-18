import os
import tempfile
import subprocess


class TestUnnamedTempFile:
    """Test class for test_unnamed_temp_file"""

    def test_unnamed_temp_file(self, fat_image):
        """Create unnamed temporary file."""
        fd, path = tempfile.mkstemp()
        os.close(fd)
        assert os.path.exists(path)
        os.remove(path)

    def test_unnamed_temp_file_cli(self, fat_image):
        """Create unnamed temporary file using CLI."""
        result = subprocess.run(["mktemp"], capture_output=True, text=True, check=True)
        path = result.stdout.strip()
        assert os.path.exists(path)
        os.remove(path)
