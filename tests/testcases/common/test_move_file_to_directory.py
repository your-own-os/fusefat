import os
import shutil
import subprocess


class TestMoveFileToDirectory:
    """Test class for test_move_file_to_directory"""

    def test_move_file_to_directory(self, fat_image):
        """Move file to subdirectory."""
        image_path, mount = fat_image
        file_path = os.path.join(mount, "file.txt")
        dir_path = os.path.join(mount, "subdir")
        os.mkdir(dir_path)
        with open(file_path, "w") as f:
            f.write("test")
        dest = os.path.join(dir_path, "file.txt")
        shutil.move(file_path, dest)
        assert not os.path.exists(file_path)
        assert os.path.exists(dest)

    def test_move_file_to_directory_cli(self, fat_image):
        """Move file to subdirectory using CLI."""
        image_path, mount = fat_image
        file_path = os.path.join(mount, "file.txt")
        dir_path = os.path.join(mount, "subdir")
        subprocess.run(["mkdir", dir_path], check=True)
        subprocess.run(["sh", "-c", f"echo 'test' > '{file_path}'"], check=True)
        dest = os.path.join(dir_path, "file.txt")
        subprocess.run(["mv", file_path, dest], check=True)
        assert not os.path.exists(file_path)
        assert os.path.exists(dest)
