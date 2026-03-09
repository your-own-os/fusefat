import os
import shutil
import subprocess


class TestDeleteDirectoryWithFiles:
    """Test class for test_delete_directory_with_files"""

    def test_delete_directory_with_files(self, fat_image):
        """Delete directory with files."""
        image_path, mount = fat_image
        dir_path = os.path.join(mount, "dir_with_files")
        os.mkdir(dir_path)
        for i in range(5):
            with open(os.path.join(dir_path, f"file{i}.txt"), "w") as f:
                f.write("test")
        shutil.rmtree(dir_path)
        assert not os.path.exists(dir_path)

    def test_delete_directory_with_files_cli(self, fat_image):
        """Delete directory with files using CLI."""
        image_path, mount = fat_image
        dir_path = os.path.join(mount, "dir_with_files")
        subprocess.run(["mkdir", dir_path], check=True)
        for i in range(5):
            subprocess.run(
                ["sh", "-c", f"echo 'test' > '{dir_path}/file{i}.txt'"], check=True
            )
        subprocess.run(["rm", "-r", dir_path], check=True)
        assert not os.path.exists(dir_path)
