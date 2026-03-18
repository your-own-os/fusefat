import os
import subprocess


class TestDeeplyNestedDirectories:
    """Test class for test_deeply_nested_directories"""

    def test_deeply_nested_directories(self, fat_image):
        """Handle deeply nested directories."""
        image_path, mount = fat_image
        path = mount
        for i in range(10):
            path = os.path.join(path, f"level_{i}")
            os.mkdir(path)
        final_path = os.path.join(path, "file.txt")
        with open(final_path, "w") as f:
            f.write("deep")
        assert os.path.exists(final_path)

    def test_deeply_nested_directories_cli(self, fat_image):
        """Handle deeply nested directories using CLI."""
        image_path, mount = fat_image
        path = mount
        for i in range(10):
            path = os.path.join(path, f"level_{i}")
            subprocess.run(["mkdir", path], check=True)
        final_path = os.path.join(path, "file.txt")
        subprocess.run(["sh", "-c", f"echo 'deep' > '{final_path}'"], check=True)
        assert os.path.exists(final_path)
