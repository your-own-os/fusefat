import os
import subprocess


class TestListDirectoryWithFiles:
    """Test class for test_list_directory_with_files"""

    def test_list_directory_with_files(self, fat_image):
        """List directory with files."""
        image_path, mount = fat_image
        for i in range(5):
            with open(os.path.join(mount, f"file{i}.txt"), "w") as f:
                f.write("test")
        entries = os.listdir(mount)
        for i in range(5):
            assert f"file{i}.txt" in entries

    def test_list_directory_with_files_cli(self, fat_image):
        """List directory with files using CLI."""
        image_path, mount = fat_image
        for i in range(5):
            path = os.path.join(mount, f"file{i}.txt")
            subprocess.run(["sh", "-c", f"echo 'test' > '{path}'"], check=True)
        result = subprocess.run(
            ["ls", mount], capture_output=True, text=True, check=True
        )
        for i in range(5):
            assert f"file{i}.txt" in result.stdout
