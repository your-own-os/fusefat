import os
import subprocess


class TestFileSync:
    """Test class for test_file_sync"""

    def test_file_sync(self, fat_image):
        """Sync file to disk."""
        image_path, mount = fat_image
        path = os.path.join(mount, "sync_test.txt")
        with open(path, "w") as f:
            f.write("test")
            os.fsync(f.fileno())
        assert os.path.exists(path)

    def test_file_sync_cli(self, fat_image):
        """Sync file to disk using CLI."""
        image_path, mount = fat_image
        path = os.path.join(mount, "sync_test.txt")
        subprocess.run(["sh", "-c", f"echo 'test' > '{path}' && sync"], check=True)
        assert os.path.exists(path)
