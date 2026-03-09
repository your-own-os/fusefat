import os
import subprocess


class TestModeWrite:
    """Test class for test_mode_write"""

    def test_mode_write(self, fat_image):
        """Open file in write mode."""
        image_path, mount = fat_image
        path = os.path.join(mount, "write_mode.txt")
        with open(path, "w") as f:
            f.write("test")

    def test_mode_write_cli(self, fat_image):
        """Open file in write mode using CLI."""
        image_path, mount = fat_image
        path = os.path.join(mount, "write_mode.txt")
        subprocess.run(["sh", "-c", f"echo 'test' > '{path}'"], check=True)
        assert os.path.exists(path)
