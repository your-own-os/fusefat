import os
import subprocess


class TestVeryLongContent:
    """Test class for test_very_long_content"""

    def test_very_long_content(self, fat_image):
        """Handle very long file content."""
        image_path, mount = fat_image
        path = os.path.join(mount, "long_content.txt")
        content = "x" * (1 * 1024 * 1024)
        with open(path, "w") as f:
            f.write(content)
        with open(path, "r") as f:
            assert len(f.read()) == 1 * 1024 * 1024

    def test_very_long_content_cli(self, fat_image):
        """Handle very long file content using CLI."""
        image_path, mount = fat_image
        path = os.path.join(mount, "long_content.txt")
        subprocess.run(
            ["dd", "if=/dev/zero", "of=" + path, "bs=1M", "count=1"], check=True
        )
        result = subprocess.run(
            ["wc", "-c", path], capture_output=True, text=True, check=True
        )
        assert result.stdout.strip().split()[0] == "1048576"
