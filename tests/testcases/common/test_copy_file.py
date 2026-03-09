import os
import shutil
import subprocess


class TestCopyFile:
    """Test class for test_copy_file"""

    def test_copy_file(self, fat_image):
        """Copy a file."""
        image_path, mount = fat_image
        src = os.path.join(mount, "source.txt")
        dst = os.path.join(mount, "dest.txt")
        with open(src, "w") as f:
            f.write("test content")
        shutil.copy2(src, dst)
        assert os.path.exists(src)
        assert os.path.exists(dst)
        with open(dst, "r") as f:
            assert f.read() == "test content"

    def test_copy_file_cli(self, fat_image):
        """Copy a file using CLI."""
        image_path, mount = fat_image
        src = os.path.join(mount, "source.txt")
        dst = os.path.join(mount, "dest.txt")
        subprocess.run(["sh", "-c", f"echo 'test content' > '{src}'"], check=True)
        subprocess.run(["cp", src, dst], check=True)
        assert os.path.exists(src)
        assert os.path.exists(dst)
        result = subprocess.run(
            ["cat", dst], capture_output=True, text=True, check=True
        )
        assert result.stdout.strip() == "test content"
