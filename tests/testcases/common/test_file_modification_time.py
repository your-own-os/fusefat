import os
import time
import subprocess


class TestFileModificationTime:
    """Test class for test_file_modification_time"""

    def test_file_modification_time(self, fat_image):
        """Get file modification time.

        FAT filesystem stores modification time with 2-second resolution.
        """
        image_path, mount = fat_image
        path = os.path.join(mount, "mtime_test.txt")
        before = time.time()
        with open(path, "w") as f:
            f.write("test")
        after = time.time()
        mtime = os.path.getmtime(path)
        assert before - 2 <= mtime <= after, (
            f"before: {before}, mtime: {mtime}, after: {after}"
        )

    def test_file_modification_time_cli(self, fat_image):
        """Get file modification time using CLI."""
        image_path, mount = fat_image
        path = os.path.join(mount, "mtime_test.txt")
        subprocess.run(["sh", "-c", f"echo 'test' > '{path}'"], check=True)
        result = subprocess.run(
            ["stat", "-c", "%Y", path], capture_output=True, text=True, check=True
        )
        assert int(result.stdout.strip()) > 0
