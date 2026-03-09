import os
import subprocess


class TestContextManager:
    """Test class for test_context_manager"""

    def test_context_manager(self, fat_image):
        """Use context manager for files."""
        image_path, mount = fat_image
        path = os.path.join(mount, "context_test.txt")
        with open(path, "w") as f:
            f.write("context test")
        with open(path, "r") as f:
            assert f.read() == "context test"

    def test_context_manager_cli(self, fat_image):
        """Use context manager for files using CLI."""
        image_path, mount = fat_image
        path = os.path.join(mount, "context_test.txt")
        subprocess.run(["sh", "-c", f"echo 'context test' > '{path}'"], check=True)
        result = subprocess.run(
            ["cat", path], capture_output=True, text=True, check=True
        )
        assert result.stdout.strip() == "context test"
