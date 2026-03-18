import os
import subprocess


class TestFileAccessTime:
    """Test class for test_file_access_time"""

    def test_file_access_time(self, fat_image):
        """Access file access time."""
        image_path, mount = fat_image
        path = os.path.join(mount, "time_test.txt")
        with open(path, "w") as f:
            f.write("test")
        atime = os.path.getatime(path)
        assert atime > 0

    def test_file_access_time_cli(self, fat_image):
        """Access file access time using CLI."""
        image_path, mount = fat_image
        path = os.path.join(mount, "time_test.txt")
        subprocess.run(["sh", "-c", f"echo 'test' > '{path}'"], check=True)
        result = subprocess.run(
            ["stat", "-c", "%X", path], capture_output=True, text=True, check=True
        )
        assert int(result.stdout.strip()) > 0
