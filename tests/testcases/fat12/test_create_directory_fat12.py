import os


class TestCreateDirectoryFat12:
    """Test class for test_create_directory_fat12"""

    def test_create_directory_fat12(self, fat_image):
        """Create directory in FAT12 filesystem."""
        image_path, mount = fat_image
        path = os.path.join(mount, "test_dir")
        os.mkdir(path)
        assert os.path.isdir(path)
