import os
import subprocess


class TestAccessSubdirectory:
    """Test class for accessing subdirectories"""

    def test_access_subdirectory(self, fat_image):
        """Access a subdirectory after creating it."""
        image_path, mount = fat_image

        # Create a subdirectory
        subdir_path = os.path.join(mount, "test_subdir")
        os.mkdir(subdir_path)
        assert os.path.isdir(subdir_path)

        # Change into the subdirectory
        original = os.getcwd()
        os.chdir(subdir_path)
        assert os.getcwd() == subdir_path
        os.chdir(original)

    def test_access_subdirectory_cli(self, fat_image):
        """Access a subdirectory after creating it using CLI."""
        image_path, mount = fat_image
        subdir_path = os.path.join(mount, "test_subdir")
        subprocess.run(["mkdir", subdir_path], check=True)
        result = subprocess.run(["test", "-d", subdir_path], capture_output=True)
        assert result.returncode == 0


class TestListSubdirectoryContents:
    """Test class for listing subdirectory contents"""

    def test_list_subdirectory_contents(self, fat_image):
        """List contents of a subdirectory."""
        image_path, mount = fat_image

        # Create a subdirectory with files
        subdir_path = os.path.join(mount, "test_subdir")
        os.mkdir(subdir_path)

        # Create files in the subdirectory
        file1 = os.path.join(subdir_path, "file1.txt")
        file2 = os.path.join(subdir_path, "file2.txt")
        open(file1, "w").write("content1")
        open(file2, "w").write("content2")

        # List contents
        contents = os.listdir(subdir_path)
        assert "file1.txt" in contents
        assert "file2.txt" in contents

    def test_list_subdirectory_contents_cli(self, fat_image):
        """List contents of a subdirectory using CLI."""
        image_path, mount = fat_image
        subdir_path = os.path.join(mount, "test_subdir")
        subprocess.run(["mkdir", subdir_path], check=True)
        subprocess.run(
            ["sh", "-c", f"echo 'content1' > '{subdir_path}/file1.txt'"], check=True
        )
        subprocess.run(
            ["sh", "-c", f"echo 'content2' > '{subdir_path}/file2.txt'"], check=True
        )
        result = subprocess.run(
            ["ls", subdir_path], capture_output=True, text=True, check=True
        )
        assert "file1.txt" in result.stdout
        assert "file2.txt" in result.stdout


class TestCreateFileInSubdirectory:
    """Test class for creating files in subdirectories"""

    def test_create_file_in_subdirectory(self, fat_image):
        """Create a file in a subdirectory."""
        image_path, mount = fat_image

        # Create a subdirectory
        subdir_path = os.path.join(mount, "test_subdir")
        os.mkdir(subdir_path)

        # Create a file in the subdirectory
        file_path = os.path.join(subdir_path, "test_file.txt")
        with open(file_path, "w") as f:
            f.write("test content")

        assert os.path.exists(file_path)
        assert os.path.isfile(file_path)

    def test_create_file_in_subdirectory_cli(self, fat_image):
        """Create a file in a subdirectory using CLI."""
        image_path, mount = fat_image
        subdir_path = os.path.join(mount, "test_subdir")
        subprocess.run(["mkdir", subdir_path], check=True)
        file_path = os.path.join(subdir_path, "test_file.txt")
        subprocess.run(["sh", "-c", f"echo 'test content' > '{file_path}'"], check=True)
        assert os.path.exists(file_path)
        assert os.path.isfile(file_path)


class TestLookupFileInSubdirectory:
    """Test class for looking up files in subdirectories"""

    def test_lookup_dot_in_subdirectory(self, fat_image):
        """Lookup . in a subdirectory."""
        image_path, mount = fat_image

        # Create a subdirectory
        subdir_path = os.path.join(mount, "test_subdir")
        os.mkdir(subdir_path)

        # Access the subdirectory and check .
        original = os.getcwd()
        os.chdir(subdir_path)
        assert os.getcwd() == subdir_path

        # The . should refer to the subdirectory
        dot_path = os.path.join(subdir_path, ".")
        assert os.path.isdir(dot_path)

        os.chdir(original)

    def test_lookup_dot_in_subdirectory_cli(self, fat_image):
        """Lookup . in a subdirectory using CLI."""
        image_path, mount = fat_image
        subdir_path = os.path.join(mount, "test_subdir")
        subprocess.run(["mkdir", subdir_path], check=True)
        result = subprocess.run(["test", "-d", subdir_path], capture_output=True)
        assert result.returncode == 0


class TestLookupDoubleDotInSubdirectory:
    """Test class for looking up .. in subdirectories"""

    def test_lookup_double_dot_in_subdirectory(self, fat_image):
        """Lookup .. in a subdirectory."""
        image_path, mount = fat_image

        # Create a subdirectory
        subdir_path = os.path.join(mount, "test_subdir")
        os.mkdir(subdir_path)

        # Access the subdirectory and check ..
        original = os.getcwd()
        os.chdir(subdir_path)

        # The .. should refer back to the parent (mount point)
        dotdot_path = os.path.join(subdir_path, "..")
        assert os.path.isdir(dotdot_path)

        os.chdir(original)

    def test_lookup_double_dot_in_subdirectory_cli(self, fat_image):
        """Lookup .. in a subdirectory using CLI."""
        image_path, mount = fat_image
        subdir_path = os.path.join(mount, "test_subdir")
        subprocess.run(["mkdir", subdir_path], check=True)
        dotdot_path = os.path.join(subdir_path, "..")
        result = subprocess.run(["test", "-d", dotdot_path], capture_output=True)
        assert result.returncode == 0


class TestDeeplyNestedDirectory:
    """Test class for deeply nested directories"""

    def test_deeply_nested_directory(self, fat_image):
        """Access deeply nested directories."""
        image_path, mount = fat_image

        # Create nested directories
        nested_path = os.path.join(mount, "a", "b", "c", "d")
        os.makedirs(nested_path)

        # Change into each level
        original = os.getcwd()

        os.chdir(mount)
        assert os.getcwd() == mount

        os.chdir("a")
        assert os.getcwd() == os.path.join(mount, "a")

        os.chdir("b")
        assert os.getcwd() == os.path.join(mount, "a", "b")

        os.chdir("c")
        assert os.getcwd() == os.path.join(mount, "a", "b", "c")

        os.chdir("d")
        assert os.getcwd() == os.path.join(mount, "a", "b", "c", "d")

        os.chdir(original)

    def test_deeply_nested_directory_cli(self, fat_image):
        """Access deeply nested directories using CLI."""
        image_path, mount = fat_image
        nested_path = os.path.join(mount, "a", "b", "c", "d")
        subprocess.run(["mkdir", "-p", nested_path], check=True)
        result = subprocess.run(["test", "-d", nested_path], capture_output=True)
        assert result.returncode == 0
