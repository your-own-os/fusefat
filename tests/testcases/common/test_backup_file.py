import os
import shutil
import subprocess


class TestBackupFile:
    """Test class for test_backup_file"""

    def test_backup_file(self, fat_image):
        """Backup file."""
        image_path, mount = fat_image
        src = os.path.join(mount, "backup_src.txt")
        dst = os.path.join(mount, "backup_dst.txt")
        with open(src, "w") as f:
            f.write("original")
        shutil.copy2(src, dst)
        with open(dst, "r") as f:
            assert f.read() == "original"

    def test_backup_file_cli(self, fat_image):
        """Backup file using CLI."""
        image_path, mount = fat_image
        src = os.path.join(mount, "backup_src.txt")
        dst = os.path.join(mount, "backup_dst.txt")
        subprocess.run(["sh", "-c", f"echo 'original' > '{src}'"], check=True)
        subprocess.run(["cp", "-p", src, dst], check=True)
        result = subprocess.run(
            ["cat", dst], capture_output=True, text=True, check=True
        )
        assert result.stdout.strip() == "original"
