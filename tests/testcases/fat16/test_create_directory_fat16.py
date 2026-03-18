import os


class TestCreateDirectoryFat16:
    """Test class for test_create_directory_fat16"""

    def test_create_directory_fat16(self, fat_image):
        """Create directory in FAT16 filesystem."""
        image_path, mount = fat_image
        path = os.path.join(mount, "test_dir")
        os.mkdir(path)
        assert os.path.isdir(path)
