import os
import subprocess


class TestModeReadBinary:
    """Test class for test_mode_read_binary"""

    def test_mode_read_binary(self, fat_image):
        """Open file in read binary mode."""
        image_path, mount = fat_image
        path = os.path.join(mount, "rb_mode.bin")
        with open(path, "wb") as f:
            f.write(b"\x00\x01\x02")
        with open(path, "rb") as f:
            assert f.read() == b"\x00\x01\x02"

    def test_mode_read_binary_cli(self, fat_image):
        """Open file in read binary mode using CLI."""
        image_path, mount = fat_image
        path = os.path.join(mount, "rb_mode.bin")
        subprocess.run(
            ["dd", "if=/dev/zero", "of=" + path, "bs=3", "count=1"], check=True
        )
        result = subprocess.run(
            ["stat", "-c", "%s", path], capture_output=True, text=True, check=True
        )
        assert result.stdout.strip() == "3"
