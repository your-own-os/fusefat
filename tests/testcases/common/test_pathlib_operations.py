from pathlib import Path
import subprocess


class TestPathlibOperations:
    """Test class for test_pathlib_operations"""

    def test_pathlib_operations(self, fat_image):
        """Use pathlib for operations."""
        image_path, mount = fat_image
        p = Path(mount) / "pathlib_test.txt"
        p.write_text("test")
        assert p.exists()
        assert p.read_text() == "test"

    def test_pathlib_operations_cli(self, fat_image):
        """Use pathlib for operations using CLI."""
        image_path, mount = fat_image
        subprocess.run(
            ["sh", "-c", f"echo 'test' > '{mount}/pathlib_test.txt'"], check=True
        )
        p = Path(mount) / "pathlib_test.txt"
        assert p.exists()
