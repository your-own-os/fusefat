import os
import subprocess


class TestIterateFiles:
    """Test class for test_iterate_files"""

    def test_iterate_files(self, fat_image):
        """Iterate over files in directory."""
        image_path, mount = fat_image
        for i in range(5):
            with open(os.path.join(mount, f"iter_{i}.txt"), "w") as f:
                f.write("test")
        count = 0
        for entry in os.listdir(mount):
            if entry.startswith("iter_"):
                count += 1
        assert count == 5

    def test_iterate_files_cli(self, fat_image):
        """Iterate over files in directory using CLI."""
        image_path, mount = fat_image
        for i in range(5):
            subprocess.run(
                ["sh", "-c", f"echo 'test' > '{mount}/iter_{i}.txt'"], check=True
            )
        result = subprocess.run(
            ["ls", mount], capture_output=True, text=True, check=True
        )
        count = sum(
            1 for entry in result.stdout.split("\n") if entry.startswith("iter_")
        )
        assert count == 5
