import os
import subprocess


class TestIterateWithFilter:
    """Test class for test_iterate_with_filter"""

    def test_iterate_with_filter(self, fat_image):
        """Iterate with filter."""
        image_path, mount = fat_image
        for i in range(5):
            with open(os.path.join(mount, f"filter_{i}.txt"), "w") as f:
                f.write("test")
            os.mkdir(os.path.join(mount, f"dir_{i}"))
        txt_files = [f for f in os.listdir(mount) if f.endswith(".txt")]
        assert len(txt_files) == 5

    def test_iterate_with_filter_cli(self, fat_image):
        """Iterate with filter using CLI."""
        image_path, mount = fat_image
        for i in range(5):
            subprocess.run(
                ["sh", "-c", f"echo 'test' > '{mount}/filter_{i}.txt'"], check=True
            )
            subprocess.run(["mkdir", f"{mount}/dir_{i}"], check=True)
        result = subprocess.run(
            ["ls", mount], capture_output=True, text=True, check=True
        )
        txt_files = [f for f in result.stdout.strip().split("\n") if f.endswith(".txt")]
        assert len(txt_files) == 5
