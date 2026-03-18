import os
import subprocess


class TestReadlines:
    """Test class for test_readlines"""

    def test_readlines(self, fat_image):
        """Read all lines."""
        image_path, mount = fat_image
        path = os.path.join(mount, "all_lines.txt")
        with open(path, "w") as f:
            f.write("line1\nline2\nline3")
        with open(path, "r") as f:
            lines = f.readlines()
            assert len(lines) == 3

    def test_readlines_cli(self, fat_image):
        """Read all lines using CLI."""
        image_path, mount = fat_image
        path = os.path.join(mount, "all_lines.txt")
        subprocess.run(
            ["sh", "-c", f"printf 'line1\\nline2\\nline3\\n' > '{path}'"], check=True
        )
        result = subprocess.run(
            ["wc", "-l", path], capture_output=True, text=True, check=True
        )
        assert result.stdout.strip().split()[0] == "3"
