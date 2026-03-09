import subprocess


class TestFilesystemType:
    """Test class for test_filesystem_type"""

    def test_filesystem_type(self, fat_image, pytestconfig):
        """Get filesystem type."""
        image_path, mount = fat_image
        result = subprocess.run(["df", "-T", mount], capture_output=True, text=True)
        lines = result.stdout.strip().split("\n")
        if len(lines) > 1:
            fs_type = lines[1].split()[1]
            expected = (
                {"fuse"}
                if pytestconfig.getoption("--backend") != "kernel"
                else {"vfat", "msdos", "fat"}
            )
            assert fs_type.lower() in expected

    def test_filesystem_type_cli(self, fat_image, pytestconfig):
        """Get filesystem type using CLI."""
        image_path, mount = fat_image
        result = subprocess.run(["df", "-T", mount], capture_output=True, text=True)
        lines = result.stdout.strip().split("\n")
        if len(lines) > 1:
            fs_type = lines[1].split()[1]
            expected = (
                {"fuse"}
                if pytestconfig.getoption("--backend") != "kernel"
                else {"vfat", "msdos", "fat"}
            )
            assert fs_type.lower() in expected
