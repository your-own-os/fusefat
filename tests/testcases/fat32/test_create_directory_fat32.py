import os


class TestCreateDirectoryFat32:
    """Test class for test_create_directory_fat32"""

    def test_create_directory_fat32(self, fat_image):
        """Create directory in FAT32 filesystem."""
        image_path, mount = fat_image
        path = os.path.join(mount, "test_dir")
        os.mkdir(path)
        assert os.path.isdir(path)
