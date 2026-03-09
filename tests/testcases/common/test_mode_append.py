import os
import subprocess


class TestModeAppend:
    """Test class for test_mode_append"""

    def test_mode_append(self, fat_image):
        """Open file in append mode."""
        image_path, mount = fat_image
        path = os.path.join(mount, "append_mode.txt")
        with open(path, "a") as f:
            f.write("test")

    def test_mode_append_cli(self, fat_image):
        """Open file in append mode using CLI."""
        image_path, mount = fat_image
        path = os.path.join(mount, "append_mode.txt")
        subprocess.run(["touch", path], check=True)
        subprocess.run(["sh", "-c", f"echo 'test' >> '{path}'"], check=True)
        result = subprocess.run(
            ["cat", path], capture_output=True, text=True, check=True
        )
        assert "test" in result.stdout
