import os
import pytest
import subprocess


class TestDirectoryNotEmptyError:
    """Test class for test_directory_not_empty_error"""

    def test_directory_not_empty_error(self, fat_image):
        """Remove non-empty directory without recursive flag."""
        image_path, mount = fat_image
        dir_path = os.path.join(mount, "nonempty")
        os.mkdir(dir_path)
        with open(os.path.join(dir_path, "file.txt"), "w") as f:
            f.write("test")
        with pytest.raises(OSError):
            os.rmdir(dir_path)

    def test_directory_not_empty_error_cli(self, fat_image):
        """Remove non-empty directory without recursive flag using CLI."""
        image_path, mount = fat_image
        dir_path = os.path.join(mount, "nonempty")
        subprocess.run(["mkdir", dir_path], check=True)
        subprocess.run(["sh", "-c", f"echo 'test' > '{dir_path}/file.txt'"], check=True)
        result = subprocess.run(["rmdir", dir_path], capture_output=True)
        assert result.returncode != 0
