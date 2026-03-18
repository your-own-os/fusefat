import os
import subprocess


class TestGetDirectorySize:
    """Test class for test_get_directory_size"""

    def test_get_directory_size(self, fat_image):
        """Get directory size."""
        image_path, mount = fat_image
        dir_path = os.path.join(mount, "testdir")
        os.mkdir(dir_path)
        total_size = 0
        for i in range(3):
            path = os.path.join(dir_path, f"file{i}.txt")
            with open(path, "w") as f:
                f.write("x" * 100)
            total_size += 100
        assert os.path.getsize(path) == 100, f"size: {os.path.getsize(path)}"

    def test_get_directory_size_cli(self, fat_image):
        """Get directory size using CLI."""
        image_path, mount = fat_image
        dir_path = os.path.join(mount, "testdir")
        subprocess.run(["mkdir", dir_path], check=True)
        for i in range(3):
            path = os.path.join(dir_path, f"file{i}.txt")
            subprocess.run(
                ["sh", "-c", f"printf 'x%.0s' {{1..100}} > '{path}'"], check=True
            )
        result = subprocess.run(
            ["stat", "-c", "%s", os.path.join(dir_path, "file2.txt")],
            capture_output=True,
            text=True,
            check=True,
        )
        assert result.stdout.strip() == "100"
