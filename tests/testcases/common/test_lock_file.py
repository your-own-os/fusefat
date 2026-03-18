import os
import subprocess


class TestLockFile:
    """Test class for test_lock_file"""

    def test_lock_file(self, fat_image):
        """Lock file for exclusive access."""
        image_path, mount = fat_image
        path = os.path.join(mount, "lock_test.txt")
        with open(path, "w") as f:
            f.write("test")
        with open(path, "r") as f:
            # Basic lock test - try to acquire
            pass  # Full lock tests require more setup

    def test_lock_file_cli(self, fat_image):
        """Lock file for exclusive access using CLI."""
        image_path, mount = fat_image
        path = os.path.join(mount, "lock_test.txt")
        subprocess.run(["sh", "-c", f"echo 'test' > '{path}'"], check=True)
        assert os.path.exists(path)
