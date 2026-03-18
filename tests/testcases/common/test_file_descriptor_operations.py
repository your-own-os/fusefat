import os
import subprocess


class TestFileDescriptorOperations:
    """Test class for test_file_descriptor_operations"""

    def test_file_descriptor_operations(self, fat_image):
        """Use low-level file descriptor."""
        image_path, mount = fat_image
        path = os.path.join(mount, "fd_test.txt")
        fd = os.open(path, os.O_WRONLY | os.O_CREAT)
        os.write(fd, b"test content")
        os.close(fd)
        assert os.path.exists(path)

    def test_file_descriptor_operations_cli(self, fat_image):
        """Use low-level file descriptor using CLI."""
        image_path, mount = fat_image
        path = os.path.join(mount, "fd_test.txt")
        subprocess.run(["sh", "-c", f"echo -n 'test content' > '{path}'"], check=True)
        assert os.path.exists(path)
