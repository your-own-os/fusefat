import os
import subprocess


class TestManySmallFiles:
    """Test class for test_many_small_files"""

    def test_many_small_files(self, fat_image):
        """Handle many small files."""
        image_path, mount = fat_image
        for i in range(100):
            path = os.path.join(mount, f"small_{i}.txt")
            with open(path, "w") as f:
                f.write(str(i))
        for i in range(100):
            path = os.path.join(mount, f"small_{i}.txt")
            assert os.path.exists(path)

    def test_many_small_files_cli(self, fat_image):
        """Handle many small files using CLI."""
        image_path, mount = fat_image
        for i in range(100):
            path = os.path.join(mount, f"small_{i}.txt")
            subprocess.run(["sh", "-c", f"echo '{i}' > '{path}'"], check=True)
        result = subprocess.run(
            ["ls", mount, "-1"], capture_output=True, text=True, check=True
        )
        files = result.stdout.strip().split("\n")
        assert (
            len([f for f in files if f.startswith("small_") and f.endswith(".txt")])
            == 100
        )
