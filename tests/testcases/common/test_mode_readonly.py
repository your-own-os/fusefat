import os
import subprocess


class TestModeReadonly:
    """Test class for test_mode_readonly"""

    def test_mode_readonly(self, fat_image):
        """Open file in read mode."""
        image_path, mount = fat_image
        path = os.path.join(mount, "read_mode.txt")
        with open(path, "w") as f:
            f.write("test")
        with open(path, "r") as f:
            assert f.read() == "test"

    def test_mode_readonly_cli(self, fat_image):
        """Open file in read mode using CLI."""
        image_path, mount = fat_image
        path = os.path.join(mount, "read_mode.txt")
        subprocess.run(["sh", "-c", f"echo 'test' > '{path}'"], check=True)
        result = subprocess.run(
            ["cat", path], capture_output=True, text=True, check=True
        )
        assert result.stdout.strip() == "test"
