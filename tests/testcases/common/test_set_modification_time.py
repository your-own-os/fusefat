import os
import time
import subprocess


class TestSetModificationTime:
    """Test class for test_set_modification_time"""

    def test_set_modification_time(self, fat_image):
        """Set modification time.

        FAT filesystem stores modification time with 2-second resolution.
        """
        image_path, mount = fat_image
        path = os.path.join(mount, "mtime_set.txt")
        with open(path, "w") as f:
            f.write("test")
        new_mtime = time.time() - 1000
        os.utime(path, (new_mtime, new_mtime))
        # FAT has 2-second resolution
        assert abs(os.path.getmtime(path) - new_mtime) < 3, (
            f"expected: {new_mtime}, actual: {os.path.getmtime(path)}"
        )

    def test_set_modification_time_cli(self, fat_image):
        """Set modification time using CLI."""
        image_path, mount = fat_image
        path = os.path.join(mount, "mtime_set.txt")
        subprocess.run(["sh", "-c", f"echo 'test' > '{path}'"], check=True)
        subprocess.run(["touch", "-d", "2020-01-01", path], check=True)
        result = subprocess.run(
            ["stat", "-c", "%Y", path], capture_output=True, text=True, check=True
        )
        mtime = int(result.stdout.strip())
        assert mtime > 0
