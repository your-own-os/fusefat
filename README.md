# fusefat

A FUSE (Filesystem in Userspace) filesystem implementation for FAT (File Allocation Table) filesystems written in Rust.

## Overview

fusefat allows you to mount FAT filesystem images (FAT12, FAT16, FAT32) on Linux systems using FUSE3.

## Homepage

https://gitee.com/your-own-os/fusefat_2

## Features

It provides exactly the same functionality as the vfat kernel module, the only difference is that fusefat runs in userspace.

## Installation

On Getnoo:
```bash
sudo emerge sys-fs/fusefat
```

### Build

The project mainly depends on these crates:
- `easy_fuser` - FUSE bindings
- `fatfs` - FAT filesystem library (version 0.3.x, not 0.4)
- `clap` - CLI argument parsing

```bash
cargo build --release
```

## Usage

```bash
fusefat <image> <mount_point> [options]
```

### Arguments

- `image` - Path to the FAT filesystem image file
- `mount_point` - Directory to mount the filesystem

### Options

- `-r, --readonly` - Mount read-only
- `-d, --debug` - Enable debug output
- `-f, --foreground` - Run in foreground instead of daemonizing
- `--allow_other` - Allow other users to access the filesystem
- `--uid <UID>` - Set the owner user ID of all files/directories
- `--gid <GID>` - Set the owner group ID of all files/directories
- `--umask <UMASK>` - Set the umask for files/directories

### Examples

Mount a FAT image read-only:
```bash
sudo ./target/release/fusefat fat.img /mnt/fat -r
```

Mount with debug output:
```bash
sudo ./target/release/fusefat fat.img /mnt/fat -d
```

Mount allowing other users:
```bash
sudo ./target/release/fusefat fat.img /mnt/fat --allow_other
```

### Running Tests
```bash
cd tests

# Run all test cases
./test

# Run specific test function (there's no duplicate test function names)
./test test_append_to_file()

# Run with fusefat backend (instead of kernel vfat)
./test --backend=fusefat test_append_to_file()

# Create FAT images manually
./mkimages
```

The test code is written in python 3.12 and above.

## License

GPLv3
