# FAT Filesystem Test Cases

This document describes the testing infrastructure for this project.

## Test Environment

- Tests use Python's pytest framework
- Each test creates its own FAT filesystem image dynamically using loop devices
- Tests mount FAT filesystem images via the kernel's FAT driver
- Each test case is in a separate file
- Tests use `su` internally (no sudo needed in test code)

## Prerequisites

Install required system packages:
```bash
# Debian/Ubuntu
sudo apt install dosfstools

# Fedora/RHEL
sudo dnf install dosfstools

# Arch Linux
sudo pacman -S dosfstools
```

## Running Tests

```bash
cd tests

# Run all tests
python -m pytest -v

# Run specific test directory
python -m pytest testcases_common -v
python -m pytest testcases_fat12 -v
python -m pytest testcases_fat16 -v
python -m pytest testcases_fat32 -v

# Run specific test file
python -m pytest testcases_common/test_create_file.py -v
```

## Test Structure

```
tests/
├── conftest.py                    # Central fixtures (fat_image, fat12_image, fat16_image, fat32_image)
├── testcases_common/               # Common tests (run on FAT32 by default)
│   └── test_*.py                  # ~95 test files
├── testcases_fat12/               # FAT12-specific tests
│   ├── conftest.py                # Uses fat12_image fixture
│   └── test_create_file_fat12.py
├── testcases_fat16/               # FAT16-specific tests
│   ├── conftest.py                # Uses fat16_image fixture
│   └── test_create_file_fat16.py
└── testcases_fat32/               # FAT32-specific tests
    ├── conftest.py                # Uses fat32_image fixture
    └── test_create_file_fat32.py
```

## Fixtures

The central `conftest.py` provides these fixtures:

| Fixture | Description |
|---------|-------------|
| `fat_image` | Default FAT32 image (32MB) |
| `fat12_image` | FAT12 image (2MB) |
| `fat16_image` | FAT16 image (16MB) |
| `fat32_image` | FAT32 image (32MB) |

## Test Categories

- File Creation (create, empty, binary, long name, special chars)
- File Read/Write (text, append, overwrite, large files)
- File Deletion (single, multiple, open file)
- Directory Creation/Deletion/Listing
- File Metadata (size, exists, is_file, is_directory)
- File Timestamps (access, modification, creation)
- File Rename/Move/Copy
- File Permissions (default, change, check)
- File Truncation/Seek
- Directory Navigation (chdir, getcwd)
- Path Operations (join, split, absolute, exists)
- Edge Cases (spaces, unicode, long content)
- File Modes (readonly, write, append, binary)
- Filesystem Info (disk usage, type)
- Concurrent Access (multiple readers, concurrent writes)
- Error Conditions (readonly location, not empty)
- Boundary Conditions (max filename length, dots)
- Iteration/Walk
- Backup/Temporary Files

## Known Limitations

- FAT filesystem does not support symbolic links (tests removed)
- FAT filesystem does not support hard links (tests removed)
- Some timestamp tests may fail due to FAT precision
- Some permission tests fail because FAT uses mount options
