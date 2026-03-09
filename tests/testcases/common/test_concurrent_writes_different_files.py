import os
import subprocess


class TestConcurrentWritesDifferentFiles:
    """Test class for test_concurrent_writes_different_files"""

    def test_concurrent_writes_different_files(self, fat_image):
        """Concurrent writes to different files."""
        image_path, mount = fat_image
        for i in range(10):
            path = os.path.join(mount, f"concurrent_{i}.txt")
            with open(path, "w") as f:
                f.write(f"content {i}")
        for i in range(10):
            path = os.path.join(mount, f"concurrent_{i}.txt")
            with open(path, "r") as f:
                assert f.read() == f"content {i}"

    def test_concurrent_writes_different_files_cli(self, fat_image):
        """Concurrent writes to different files using CLI."""
        image_path, mount = fat_image
        for i in range(10):
            path = os.path.join(mount, f"concurrent_{i}.txt")
            subprocess.run(["sh", "-c", f"echo 'content {i}' > '{path}'"], check=True)
        for i in range(10):
            path = os.path.join(mount, f"concurrent_{i}.txt")
            result = subprocess.run(
                ["cat", path], capture_output=True, text=True, check=True
            )
            assert result.stdout.strip() == f"content {i}"
