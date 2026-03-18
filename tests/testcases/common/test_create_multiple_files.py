import os
import subprocess


class TestCreateMultipleFiles:
    """Test class for test_create_multiple_files"""

    def test_create_multiple_files(self, fat_image):
        """Create multiple files in same directory."""
        image_path, mount = fat_image
        for i in range(10):
            path = os.path.join(mount, f"file_{i}.txt")
            with open(path, "w") as f:
                f.write(f"content {i}")
        for i in range(10):
            assert os.path.exists(os.path.join(mount, f"file_{i}.txt"))

    def test_create_multiple_files_cli(self, fat_image):
        """Create multiple files in same directory using CLI."""
        image_path, mount = fat_image
        for i in range(10):
            path = os.path.join(mount, f"file_{i}.txt")
            subprocess.run(["sh", "-c", f"echo 'content {i}' > '{path}'"], check=True)
        for i in range(10):
            assert os.path.exists(os.path.join(mount, f"file_{i}.txt"))
