import os
import subprocess


class TestWalkDirectoryTree:
    """Test class for test_walk_directory_tree"""

    def test_walk_directory_tree(self, fat_image):
        """Walk directory tree."""
        image_path, mount = fat_image
        # Create nested structure
        for i in range(3):
            dir_path = os.path.join(mount, f"level0_{i}")
            os.mkdir(dir_path)
            for j in range(2):
                subdir = os.path.join(dir_path, f"level1_{j}")
                os.mkdir(subdir)
        dirs_walked = []
        for root, dirs, files in os.walk(mount):
            dirs_walked.extend(dirs)
        assert len(dirs_walked) >= 5

    def test_walk_directory_tree_cli(self, fat_image):
        """Walk directory tree using CLI."""
        image_path, mount = fat_image
        for i in range(3):
            dir_path = os.path.join(mount, f"level0_{i}")
            subprocess.run(["mkdir", dir_path], check=True)
            for j in range(2):
                subdir = os.path.join(dir_path, f"level1_{j}")
                subprocess.run(["mkdir", subdir], check=True)
        result = subprocess.run(
            ["find", mount, "-type", "d"], capture_output=True, text=True, check=True
        )
        dirs = result.stdout.strip().split("\n")
        assert len(dirs) >= 6
