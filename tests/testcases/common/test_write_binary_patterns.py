import os
import subprocess


class TestWriteBinaryPatterns:
    """Test class for test_write_binary_patterns"""

    def test_write_binary_patterns(self, fat_image):
        """Write various binary patterns."""
        image_path, mount = fat_image
        path = os.path.join(mount, "patterns.bin")
        patterns = [
            bytes([0] * 100),
            bytes([255] * 100),
            bytes(range(100)),
            bytes([i % 256 for i in range(100)]),
        ]
        with open(path, "wb") as f:
            for p in patterns:
                f.write(p)
        assert os.path.getsize(path) == 400, f"size: {os.path.getsize(path)}"

    def test_write_binary_patterns_cli(self, fat_image):
        """Write various binary patterns using CLI."""
        image_path, mount = fat_image
        path = os.path.join(mount, "patterns.bin")
        subprocess.run(
            ["dd", "if=/dev/zero", "of=" + path, "bs=100", "count=4"], check=True
        )
        assert os.path.getsize(path) == 400
