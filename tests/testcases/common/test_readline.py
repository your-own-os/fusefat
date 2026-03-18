import os
import subprocess


class TestReadline:
    """Test class for test_readline"""

    def test_readline(self, fat_image):
        """Read single line."""
        image_path, mount = fat_image
        path = os.path.join(mount, "lines.txt")
        with open(path, "w") as f:
            f.write("line1\nline2\nline3")
        with open(path, "r") as f:
            assert f.readline() == "line1\n"

    def test_readline_cli(self, fat_image):
        """Read single line using CLI."""
        image_path, mount = fat_image
        path = os.path.join(mount, "lines.txt")
        subprocess.run(
            ["sh", "-c", f"printf 'line1\\nline2\\nline3' > '{path}'"], check=True
        )
        result = subprocess.run(
            ["head", "-n", "1", path], capture_output=True, text=True, check=True
        )
        assert result.stdout.strip() == "line1"
