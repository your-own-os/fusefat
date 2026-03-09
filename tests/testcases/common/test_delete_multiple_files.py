import os
import subprocess


class TestDeleteMultipleFiles:
    """Test class for test_delete_multiple_files"""

    def test_delete_multiple_files(self, fat_image):
        """Delete multiple files."""
        image_path, mount = fat_image
        files = []
        for i in range(5):
            path = os.path.join(mount, f"delete_{i}.txt")
            with open(path, "w") as f:
                f.write("test")
            files.append(path)
        for f in files:
            os.remove(f)
        for f in files:
            assert not os.path.exists(f)

    def test_delete_multiple_files_cli(self, fat_image):
        """Delete multiple files using CLI."""
        image_path, mount = fat_image
        files = []
        for i in range(5):
            path = os.path.join(mount, f"delete_{i}.txt")
            subprocess.run(["sh", "-c", f"echo 'test' > '{path}'"], check=True)
            files.append(path)
        for f in files:
            subprocess.run(["rm", f], check=True)
        for f in files:
            assert not os.path.exists(f)
