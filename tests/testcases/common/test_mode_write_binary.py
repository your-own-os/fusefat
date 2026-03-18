import os
import subprocess


class TestModeWriteBinary:
    """Test class for test_mode_write_binary"""

    def test_mode_write_binary(self, fat_image):
        """Open file in write binary mode."""
        image_path, mount = fat_image
        path = os.path.join(mount, "wb_mode.bin")
        with open(path, "wb") as f:
            f.write(b"\x00\x01\x02")

    def test_mode_write_binary_cli(self, fat_image):
        """Open file in write binary mode using CLI."""
        image_path, mount = fat_image
        path = os.path.join(mount, "wb_mode.bin")
        subprocess.run(
            ["dd", "if=/dev/zero", "of=" + path, "bs=3", "count=1"], check=True
        )
        assert os.path.exists(path)
