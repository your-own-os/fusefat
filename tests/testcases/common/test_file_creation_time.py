import os
import subprocess


class TestFileCreationTime:
    """Test class for test_file_creation_time"""

    def test_file_creation_time(self, fat_image):
        """Get file creation time (ctime)."""
        image_path, mount = fat_image
        path = os.path.join(mount, "ctime_test.txt")
        with open(path, "w") as f:
            f.write("test")
        ctime = os.path.getctime(path)
        assert ctime > 0

    def test_file_creation_time_cli(self, fat_image):
        """Get file creation time using CLI."""
        image_path, mount = fat_image
        path = os.path.join(mount, "ctime_test.txt")
        subprocess.run(["sh", "-c", f"echo 'test' > '{path}'"], check=True)
        result = subprocess.run(
            ["stat", "-c", "%Y", path], capture_output=True, text=True, check=True
        )
        assert int(result.stdout.strip()) > 0
