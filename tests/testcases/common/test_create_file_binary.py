import os
import subprocess


class TestCreateFileBinary:
    """Test class for test_create_file_binary"""

    def test_create_file_binary(self, fat_image):
        """Create binary file."""
        image_path, mount = fat_image
        path = os.path.join(mount, "binary.bin")
        data = bytes(range(256))
        with open(path, "wb") as f:
            f.write(data)
        assert os.path.exists(path)
        assert os.path.getsize(path) == 256, f"size: {os.path.getsize(path)}"

    def test_create_file_binary_cli(self, fat_image):
        """Create binary file using CLI."""
        image_path, mount = fat_image
        path = os.path.join(mount, "binary.bin")
        subprocess.run(
            ["dd", "if=/dev/urandom", "of=" + path, "bs=256", "count=1"], check=True
        )
        assert os.path.exists(path)
        assert os.path.getsize(path) == 256
