import shutil
import subprocess


class TestDiskUsage:
    """Test class for test_disk_usage"""

    def test_disk_usage(self, fat_image):
        """Get disk usage."""
        image_path, mount = fat_image
        usage = shutil.disk_usage(mount)
        assert usage.total > 0
        assert usage.used >= 0
        assert usage.free > 0

    def test_disk_usage_cli(self, fat_image):
        """Get disk usage using CLI."""
        image_path, mount = fat_image
        result = subprocess.run(
            ["df", mount], capture_output=True, text=True, check=True
        )
        assert len(result.stdout) > 0
