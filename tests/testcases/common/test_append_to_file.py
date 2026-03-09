import os
import subprocess


class TestAppendToFile:
    def test_append_to_file(self, fat_image):
        """Append content to file."""
        image_path, mount = fat_image
        path = os.path.join(mount, "append.txt")
        with open(path, "w") as f:
            f.write("first")
        with open(path, "a") as f:
            f.write(" second")
        with open(path, "r") as f:
            assert f.read() == "first second"

    def test_append_to_file_cli(self, fat_image):
        """Append content to file using CLI."""
        image_path, mount = fat_image
        path = os.path.join(mount, "append.txt")
        subprocess.run(["sh", "-c", f"echo -n 'first' > '{path}'"], check=True)
        subprocess.run(["sh", "-c", f"echo ' second' >> '{path}'"], check=True)
        result = subprocess.run(
            ["cat", path], capture_output=True, text=True, check=True
        )
        assert result.stdout.strip() == "first second"
