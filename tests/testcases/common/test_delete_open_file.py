import os
import pytest
import subprocess


class TestDeleteOpenFile:
    """Test class for test_delete_open_file"""

    def test_delete_open_file(self, fat_image):
        """Deleting an open file invalidates later writes on FAT."""
        image_path, mount = fat_image
        path = os.path.join(mount, "open_delete.txt")
        f = open(path, "w")
        try:
            f.write("test")
            os.remove(path)
            with pytest.raises(OSError):
                f.close()
        finally:
            try:
                f.close()
            except OSError:
                pass
        assert not os.path.exists(path)

    def test_delete_open_file_cli(self, fat_image):
        """Delete file while open using CLI."""
        image_path, mount = fat_image
        path = os.path.join(mount, "open_delete.txt")
        subprocess.run(
            ["sh", "-c", f"echo 'test' > '{path}' && rm '{path}'"], check=True
        )
        assert not os.path.exists(path)
