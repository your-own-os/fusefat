import os
import shutil
import subprocess


class TestCopyDirectory:
    """Test class for test_copy_directory"""

    def test_copy_directory(self, fat_image):
        """Copy directory."""
        image_path, mount = fat_image
        src = os.path.join(mount, "src_dir")
        dst = os.path.join(mount, "dst_dir")
        os.mkdir(src)
        with open(os.path.join(src, "file.txt"), "w") as f:
            f.write("test")
        os.mkdir(dst)
        shutil.copy2(os.path.join(src, "file.txt"), os.path.join(dst, "file.txt"))
        assert os.path.exists(src)
        assert os.path.exists(dst)
        assert os.path.exists(os.path.join(dst, "file.txt"))

    def test_copy_directory_cli(self, fat_image):
        """Copy directory using CLI."""
        image_path, mount = fat_image
        src = os.path.join(mount, "src_dir")
        dst = os.path.join(mount, "dst_dir")
        subprocess.run(["mkdir", src], check=True)
        subprocess.run(["sh", "-c", f"echo 'test' > '{src}/file.txt'"], check=True)
        subprocess.run(["cp", "-r", src, dst], check=True)
        assert os.path.exists(src)
        assert os.path.exists(dst)
        assert os.path.exists(os.path.join(dst, "file.txt"))
