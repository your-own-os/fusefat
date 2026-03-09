import os
import subprocess


class TestWriteLines:
    """Test class for test_write_lines"""

    def test_write_lines(self, fat_image):
        """Write multiple lines."""
        image_path, mount = fat_image
        path = os.path.join(mount, "write_lines.txt")
        lines = ["line1\n", "line2\n", "line3"]
        with open(path, "w") as f:
            f.writelines(lines)
        with open(path, "r") as f:
            content = f.read()
            assert "line1" in content
            assert "line2" in content
            assert "line3" in content

    def test_write_lines_cli(self, fat_image):
        """Write multiple lines using CLI."""
        image_path, mount = fat_image
        path = os.path.join(mount, "write_lines.txt")
        subprocess.run(
            ["sh", "-c", f"printf 'line1\\nline2\\nline3' > '{path}'"], check=True
        )
        result = subprocess.run(
            ["cat", path], capture_output=True, text=True, check=True
        )
        assert "line1" in result.stdout
        assert "line2" in result.stdout
        assert "line3" in result.stdout
