import os
import shutil
import subprocess


class TestMoveDirectory:
    """Test class for test_move_directory"""

    def test_move_directory(self, fat_image):
        """Move directory."""
        image_path, mount = fat_image
        src = os.path.join(mount, "src_dir")
        dst = os.path.join(mount, "dst_dir")
        os.mkdir(src)
        with open(os.path.join(src, "file.txt"), "w") as f:
            f.write("test")
        shutil.move(src, dst)
        assert not os.path.exists(src)
        assert os.path.exists(dst)
        assert os.path.exists(os.path.join(dst, "file.txt"))

    def test_move_directory_cli(self, fat_image):
        """Move directory using CLI."""
        image_path, mount = fat_image
        src = os.path.join(mount, "src_dir")
        dst = os.path.join(mount, "dst_dir")
        subprocess.run(["mkdir", src], check=True)
        subprocess.run(["sh", "-c", f"echo 'test' > '{src}/file.txt'"], check=True)
        subprocess.run(["mv", src, dst], check=True)
        assert not os.path.exists(src)
        assert os.path.exists(dst)
        assert os.path.exists(os.path.join(dst, "file.txt"))
