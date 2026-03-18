use std::fs::File;
use std::path::PathBuf;

use anyhow::{Context, Result};
use clap::{ArgAction, Parser, ValueHint};
use easy_fuser::{mount, prelude::MountOption};
use env_logger::Env;
use fatfs::{FileSystem, FsOptions};
use log::{debug, info};

mod error;
mod fatfs_fuse;

#[derive(Debug, Parser)]
#[command(author = "FUSE FATFS Project", version = "0.1.0", about = "Mounts a FAT filesystem image using FUSE", long_about = None)]
struct Args {
    #[arg(required = true, value_hint = ValueHint::FilePath)]
    image: String,

    #[arg(required = true, value_hint = ValueHint::DirPath)]
    mount_point: String,

    #[arg(short = 'r', long, action = ArgAction::SetTrue)]
    readonly: bool,

    #[arg(short = 'd', long, action = ArgAction::SetTrue)]
    debug: bool,

    #[arg(short = 'f', long, action = ArgAction::SetTrue)]
    foreground: bool,

    #[arg(long, action = ArgAction::SetTrue)]
    allow_other: bool,
}

fn unmount(mount_point: &PathBuf) {
    let result = std::process::Command::new("fusermount")
        .args(["-u", &mount_point.to_string_lossy()])
        .output();

    match result {
        Ok(output) => {
            if output.status.success() {
                info!("Successfully unmounted {}", mount_point.display());
            } else {
                let stderr = String::from_utf8_lossy(&output.stderr);
                info!("Unmount warning: {}", stderr);
            }
        }
        Err(e) => {
            info!("Failed to unmount: {}", e);
        }
    }
}

struct MountGuard {
    mount_point: PathBuf,
}

impl Drop for MountGuard {
    fn drop(&mut self) {
        unmount(&self.mount_point);
    }
}

fn main() -> Result<()> {
    let args = Args::parse();

    let log_level = if args.debug { "debug" } else { "info" };
    env_logger::Builder::from_env(Env::default().default_filter_or(log_level)).init();

    if args.debug {
        debug!("Debug mode enabled");
    }

    let mount_point_path = PathBuf::from(&args.mount_point);
    if !mount_point_path.exists() || !mount_point_path.is_dir() {
        return Err(anyhow::anyhow!(
            "Mount point '{}' does not exist or is not a directory",
            args.mount_point
        ));
    }

    info!(
        "Mounting FAT image '{}' to '{}'",
        args.image, args.mount_point
    );

    let image_file = File::options()
        .read(true)
        .write(!args.readonly)
        .open(&args.image)
        .with_context(|| format!("Failed to open image file '{}'", args.image))?;

    let fs_options = FsOptions::new();
    let fs = FileSystem::new(image_file, fs_options)
        .with_context(|| "Failed to mount FAT filesystem")?;

    let filesystem = fatfs_fuse::FatGsFuse::new(fs, args.readonly);

    let mut mount_options = vec![MountOption::FSName("fusefat".to_string())];

    if args.allow_other {
        mount_options.push(MountOption::AllowOther);
    }

    if args.readonly {
        mount_options.push(MountOption::RO);
    } else {
        mount_options.push(MountOption::RW);
    }

    info!(
        "Mounting with options: readonly={}, debug={}, allow_other={}, mount_options={:?}",
        args.readonly, args.debug, args.allow_other, mount_options
    );

    let _guard = MountGuard {
        mount_point: mount_point_path.clone(),
    };

    mount(filesystem, &mount_point_path, &mount_options)?;

    info!("Filesystem mounted successfully");

    Ok(())
}
