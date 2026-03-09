use std::io;
use std::path::{Path, PathBuf};

use libc;
use thiserror::Error;

#[derive(Error, Debug)]
pub enum FatFsError {
    #[error("File not found: {0}")]
    FileNotFound(String),

    #[error("Directory not found: {0}")]
    DirectoryNotFound(String),

    #[error("Not a directory")]
    NotADirectory,

    #[error("Not a file")]
    NotAFile,

    #[error("Permission denied")]
    PermissionDenied,

    #[error("Read-only filesystem")]
    ReadOnlyFilesystem,

    #[error("I/O error: {0}")]
    IoError(#[from] io::Error),

    #[error("Path not found: {0}")]
    PathNotFound(PathBuf),

    #[error("Invalid path: {0}")]
    InvalidPath(String),

    #[error("File already exists: {0}")]
    FileExists(String),

    #[error("Directory not empty: {0}")]
    DirectoryNotEmpty(String),

    #[error("End of file")]
    EndOfFile,

    #[error("Unsupported operation")]
    UnsupportedOperation,

    #[error("Bad file descriptor")]
    BadFileDescriptor,

    #[error("Out of memory")]
    OutOfMemory,

    #[error("Too many open files")]
    TooManyOpenFiles,

    #[error("Operation not permitted")]
    OperationNotPermitted,

    #[error("Invalid argument: {0}")]
    InvalidArgument(String),
}

impl FatFsError {
    pub fn file_not_found<P: AsRef<Path>>(path: P) -> Self {
        Self::FileNotFound(path.as_ref().display().to_string())
    }

    pub fn directory_not_found<P: AsRef<Path>>(path: P) -> Self {
        Self::DirectoryNotFound(path.as_ref().display().to_string())
    }

    pub fn path_not_found<P: AsRef<Path>>(path: P) -> Self {
        Self::PathNotFound(path.as_ref().to_path_buf())
    }

    pub fn file_exists<P: AsRef<Path>>(path: P) -> Self {
        Self::FileExists(path.as_ref().display().to_string())
    }

    pub fn directory_not_empty<P: AsRef<Path>>(path: P) -> Self {
        Self::DirectoryNotEmpty(path.as_ref().display().to_string())
    }

    pub fn invalid_path<S: Into<String>>(path: S) -> Self {
        Self::InvalidPath(path.into())
    }

    pub fn invalid_argument<S: Into<String>>(arg: S) -> Self {
        Self::InvalidArgument(arg.into())
    }
}

impl From<FatFsError> for i32 {
    fn from(error: FatFsError) -> Self {
        match error {
            FatFsError::FileNotFound(_) => libc::ENOENT,
            FatFsError::DirectoryNotFound(_) => libc::ENOENT,
            FatFsError::NotADirectory => libc::ENOTDIR,
            FatFsError::NotAFile => libc::EISDIR,
            FatFsError::PermissionDenied => libc::EACCES,
            FatFsError::ReadOnlyFilesystem => libc::EROFS,
            FatFsError::IoError(e) => e.raw_os_error().unwrap_or(libc::EIO),
            FatFsError::PathNotFound(_) => libc::ENOENT,
            FatFsError::InvalidPath(_) => libc::ENOENT,
            FatFsError::FileExists(_) => libc::EEXIST,
            FatFsError::DirectoryNotEmpty(_) => libc::ENOTEMPTY,
            FatFsError::EndOfFile => libc::EIO,
            FatFsError::UnsupportedOperation => libc::ENOSYS,
            FatFsError::BadFileDescriptor => libc::EBADF,
            FatFsError::OutOfMemory => libc::ENOMEM,
            FatFsError::TooManyOpenFiles => libc::EMFILE,
            FatFsError::OperationNotPermitted => libc::EPERM,
            FatFsError::InvalidArgument(_) => libc::EINVAL,
        }
    }
}

// Helper macro for error handling
#[macro_export]
macro_rules! fatfs_result {
    ($expr:expr) => {
        $expr.map_err(|e| {
            log::debug!("Error: {}", e);
            e.into()
        })
    };
}

// Helper macro for logging errors
#[macro_export]
macro_rules! log_error {
    ($expr:expr, $msg:expr) => {
        match $expr {
            Ok(v) => Ok(v),
            Err(e) => {
                log::error!("{}: {}", $msg, e);
                Err(e)
            }
        }
    };
}

// Helper macro for logging warnings
#[macro_export]
macro_rules! log_warning {
    ($expr:expr, $msg:expr) => {
        match $expr {
            Ok(v) => Ok(v),
            Err(e) => {
                log::warn!("{}: {}", $msg, e);
                Err(e)
            }
        }
    };
}
