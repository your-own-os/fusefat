use std::cell::RefCell;
use std::collections::HashSet;
use std::ffi::{OsStr, OsString};
use std::fs::File as StdFile;
use std::io::{Read, Seek, SeekFrom, Write};
use std::path::Path;
use std::path::PathBuf;
use std::time::{Duration, SystemTime, UNIX_EPOCH};

use chrono::{Datelike, Local, NaiveDate, TimeZone, Timelike};
use easy_fuser::{
    templates::DefaultFuseHandler,
    types::{
        arguments::{FileAttribute, RequestInfo, SetAttrRequest, StatFs},
        errors::{FuseResult, PosixError},
        file_handle::{BorrowedFileHandle, OwnedFileHandle},
        flags::{
            AccessMask, FUSEOpenFlags, FUSEOpenResponseFlags, FUSESetXAttrFlags, FUSEWriteFlags,
            OpenFlags, RenameFlags,
        },
        FileKind, KernelConfig,
    },
    FuseHandler,
};
use fatfs::{Date, DateTime, Dir, DirEntry, FileSystem, Time};
use fuser::TimeOrNow;

pub struct FatGsFuse {
    fs: FileSystem<StdFile>,
    inner: DefaultFuseHandler,
    read_only: bool,
    open_files: RefCell<HashSet<u64>>,
    next_file_handle: RefCell<u64>,
}

impl FatGsFuse {
    pub fn new(fs: FileSystem<StdFile>, read_only: bool) -> Self {
        Self {
            fs,
            inner: DefaultFuseHandler::new(),
            read_only,
            open_files: RefCell::new(HashSet::new()),
            next_file_handle: RefCell::new(1),
        }
    }

    fn allocate_handle(&self) -> u64 {
        let mut handle = self.next_file_handle.borrow_mut();
        let id = *handle;
        *handle += 1;
        id
    }

    fn current_uid() -> u32 {
        unsafe { libc::getuid() }
    }

    fn current_gid() -> u32 {
        unsafe { libc::getgid() }
    }

    fn is_root_path(path: &Path) -> bool {
        path.as_os_str().is_empty() || path == Path::new("/")
    }

    fn path_to_dir(&self, path: &Path) -> Result<Dir<'_, StdFile>, PosixError> {
        let mut dir = self.fs.root_dir();
        for component in path
            .iter()
            .filter(|component| *component != OsStr::new("/"))
        {
            let name = component
                .to_str()
                .ok_or_else(|| PosixError::new(libc::EINVAL, "Invalid path component"))?;
            dir = dir
                .open_dir(name)
                .map_err(|_| PosixError::new(libc::ENOENT, "Directory not found"))?;
        }
        Ok(dir)
    }

    fn local_datetime_to_system_time(date: NaiveDate, time: Time) -> SystemTime {
        let naive = match date.and_hms_milli_opt(
            time.hour.into(),
            time.min.into(),
            time.sec.into(),
            time.millis.into(),
        ) {
            Some(naive) => naive,
            None => return UNIX_EPOCH,
        };

        let local = match Local.from_local_datetime(&naive).single() {
            Some(local) => local,
            None => return UNIX_EPOCH,
        };

        let secs = local.timestamp();
        if secs < 0 {
            return UNIX_EPOCH;
        }

        UNIX_EPOCH
            + Duration::from_secs(secs as u64)
            + Duration::from_nanos(u64::from(local.timestamp_subsec_nanos()))
    }

    fn fat_date_to_system_time(date: Date) -> SystemTime {
        let naive =
            match NaiveDate::from_ymd_opt(date.year.into(), date.month.into(), date.day.into()) {
                Some(naive) => naive,
                None => return UNIX_EPOCH,
            };

        Self::local_datetime_to_system_time(
            naive,
            Time {
                hour: 0,
                min: 0,
                sec: 0,
                millis: 0,
            },
        )
    }

    fn fat_datetime_to_system_time(date_time: DateTime) -> SystemTime {
        let naive = match NaiveDate::from_ymd_opt(
            date_time.date.year.into(),
            date_time.date.month.into(),
            date_time.date.day.into(),
        ) {
            Some(naive) => naive,
            None => return UNIX_EPOCH,
        };

        Self::local_datetime_to_system_time(naive, date_time.time)
    }

    fn build_attr(is_dir: bool, size: u64, atime: SystemTime, mtime: SystemTime, ctime: SystemTime, crtime: SystemTime) -> FileAttribute {
        FileAttribute {
            size,
            blocks: (size + 511) / 512,
            atime,
            mtime,
            ctime,
            crtime,
            kind: if is_dir {
                FileKind::Directory
            } else {
                FileKind::RegularFile
            },
            perm: 0o755,
            nlink: if is_dir { 2 } else { 1 },
            uid: Self::current_uid(),
            gid: Self::current_gid(),
            rdev: 0,
            blksize: 512,
            flags: 0,
            ttl: None,
            generation: Some(1),
        }
    }

    fn root_attr() -> FileAttribute {
        let now = SystemTime::now();
        Self::build_attr(true, 0, now, now, now, now)
    }

    fn entry_attr(entry: &DirEntry<'_, StdFile>) -> FileAttribute {
        let created = Self::fat_datetime_to_system_time(entry.created());
        let accessed = Self::fat_date_to_system_time(entry.accessed());
        let modified = Self::fat_datetime_to_system_time(entry.modified());
        Self::build_attr(
            entry.is_dir(),
            entry.len(),
            accessed,
            modified,
            modified,
            created,
        )
    }

    fn file_parent_and_name(file_id: &Path) -> Result<(PathBuf, &str), PosixError> {
        let parent = file_id
            .parent()
            .ok_or_else(|| PosixError::new(libc::EINVAL, "No parent"))?
            .to_path_buf();
        let name = file_id
            .file_name()
            .ok_or_else(|| PosixError::new(libc::EINVAL, "No filename"))?
            .to_str()
            .ok_or_else(|| PosixError::new(libc::EINVAL, "Invalid filename"))?;
        Ok((parent, name))
    }

    fn system_time_to_fat_datetime(time: SystemTime) -> Result<DateTime, PosixError> {
        let duration = time
            .duration_since(UNIX_EPOCH)
            .map_err(|_| PosixError::new(libc::EINVAL, "Invalid timestamp"))?;
        let local = Local
            .timestamp_opt(duration.as_secs() as i64, duration.subsec_nanos())
            .single()
            .ok_or_else(|| PosixError::new(libc::EINVAL, "Invalid timestamp"))?;
        Ok(DateTime {
            date: Date {
                year: local.year() as u16,
                month: local.month() as u16,
                day: local.day() as u16,
            },
            time: Time {
                hour: local.hour() as u16,
                min: local.minute() as u16,
                sec: local.second() as u16,
                millis: (local.nanosecond() / 1_000_000) as u16,
            },
        })
    }

    fn set_time_value(value: TimeOrNow) -> Result<SystemTime, PosixError> {
        match value {
            TimeOrNow::SpecificTime(time) => Ok(time),
            TimeOrNow::Now => Ok(SystemTime::now()),
        }
    }
}

impl FuseHandler<PathBuf> for FatGsFuse {
    fn get_inner(&self) -> &dyn FuseHandler<PathBuf> {
        &self.inner
    }

    fn init(&self, _req: &RequestInfo, _config: &mut KernelConfig) -> FuseResult<()> {
        Ok(())
    }

    fn destroy(&self) {
        // No cleanup needed
    }

    fn listxattr(&self, _req: &RequestInfo, _file_id: PathBuf, _size: u32) -> FuseResult<Vec<u8>> {
        Ok(Vec::new())
    }

    fn getxattr(&self, _req: &RequestInfo, _file_id: PathBuf, _name: &OsStr, _size: u32) -> FuseResult<Vec<u8>> {
        Err(PosixError::new(libc::ENODATA, "No extended attributes"))
    }

    fn setxattr(&self, _req: &RequestInfo, _file_id: PathBuf, _name: &OsStr, _value: Vec<u8>, _flags: FUSESetXAttrFlags, _position: u32) -> FuseResult<()> {
        Err(PosixError::new(
            libc::ENOTSUP,
            "Extended attributes not supported",
        ))
    }

    fn removexattr(&self, _req: &RequestInfo, _file_id: PathBuf, _name: &OsStr) -> FuseResult<()> {
        Err(PosixError::new(
            libc::ENOTSUP,
            "Extended attributes not supported",
        ))
    }

    fn lookup(&self, _req: &RequestInfo, parent: PathBuf, name: &OsStr) -> FuseResult<FileAttribute> {
        let name_str = name
            .to_str()
            .ok_or_else(|| PosixError::new(libc::EINVAL, "Invalid name"))?;

        if name_str == "." || name_str == ".." {
            return Ok(Self::root_attr());
        }

        let parent_dir = self.path_to_dir(&parent)?;

        for entry in parent_dir.iter() {
            if let Ok(e) = entry {
                if e.file_name() == name_str {
                    return Ok(Self::entry_attr(&e));
                }
            }
        }

        Err(PosixError::new(libc::ENOENT, "Entry not found"))
    }

    fn getattr(&self, req: &RequestInfo, file_id: PathBuf, _file_handle: Option<BorrowedFileHandle<'_>>) -> FuseResult<FileAttribute> {
        if Self::is_root_path(&file_id) {
            return Ok(Self::root_attr());
        }

        let parent = file_id
            .parent()
            .unwrap_or_else(|| Path::new("/"))
            .to_path_buf();
        let name = file_id
            .file_name()
            .ok_or_else(|| PosixError::new(libc::EINVAL, "No filename"))?;
        self.lookup(req, parent, name)
    }

    fn setattr(&self, req: &RequestInfo, file_id: PathBuf, attrs: SetAttrRequest) -> FuseResult<FileAttribute> {
        if Self::is_root_path(&file_id) {
            return Ok(Self::root_attr());
        }

        let (parent, name) = Self::file_parent_and_name(&file_id)?;
        let parent_dir = self.path_to_dir(&parent)?;

        if let Some(size) = attrs.size {
            let mut file = parent_dir
                .open_file(name)
                .map_err(|_| PosixError::new(libc::ENOENT, "File not found"))?;
            let current_len = file
                .seek(SeekFrom::End(0))
                .map_err(|_| PosixError::new(libc::EIO, "Seek failed"))?;
            if size == 0 {
                file.seek(SeekFrom::Start(0))
                    .map_err(|_| PosixError::new(libc::EIO, "Seek failed"))?;
                file.truncate()
                    .map_err(|_| PosixError::new(libc::EIO, "Truncate failed"))?;
            } else if size < current_len {
                file.seek(SeekFrom::Start(size))
                    .map_err(|_| PosixError::new(libc::EIO, "Seek failed"))?;
                file.truncate()
                    .map_err(|_| PosixError::new(libc::EIO, "Truncate failed"))?;
            }
        }

        if attrs.mtime.is_some() || attrs.atime.is_some() {
            let mut file = parent_dir
                .open_file(name)
                .map_err(|_| PosixError::new(libc::ENOENT, "File not found"))?;

            if let Some(mtime) = attrs.mtime {
                let mtime = Self::set_time_value(mtime)?;
                let fat_mtime = Self::system_time_to_fat_datetime(mtime)?;
                file.set_modified(fat_mtime);
            }

            if let Some(atime) = attrs.atime {
                let atime = Self::set_time_value(atime)?;
                let fat_atime = Self::system_time_to_fat_datetime(atime)?;
                file.set_accessed(fat_atime.date);
            }

            file.flush()
                .map_err(|_| PosixError::new(libc::EIO, "Flush failed"))?;
        }

        self.getattr(req, file_id, None)
    }

    fn readdir(&self, _req: &RequestInfo, dir_path: PathBuf, _file_handle: BorrowedFileHandle<'_>) -> FuseResult<Vec<(OsString, FileKind)>> {
        let dir = self.path_to_dir(&dir_path)?;

        let mut entries = Vec::new();
        entries.push((OsString::from("."), FileKind::Directory));
        entries.push((OsString::from(".."), FileKind::Directory));

        for entry in dir.iter() {
            if let Ok(e) = entry {
                let name = e.file_name();
                if name != "." && name != ".." {
                    entries.push((
                        OsString::from(name),
                        if e.is_dir() {
                            FileKind::Directory
                        } else {
                            FileKind::RegularFile
                        },
                    ));
                }
            }
        }

        Ok(entries)
    }

    fn opendir(&self, _req: &RequestInfo, _file_id: PathBuf, _flags: OpenFlags) -> FuseResult<(OwnedFileHandle, FUSEOpenResponseFlags)> {
        let handle = self.allocate_handle();
        self.open_files.borrow_mut().insert(handle);
        Ok((
            unsafe { OwnedFileHandle::from_raw(handle) },
            FUSEOpenResponseFlags::empty(),
        ))
    }

    fn releasedir(&self, _req: &RequestInfo, _file_id: PathBuf, file_handle: OwnedFileHandle, _flags: OpenFlags) -> FuseResult<()> {
        self.open_files
            .borrow_mut()
            .remove(&file_handle.borrow().as_raw());
        Ok(())
    }

    fn open(&self, _req: &RequestInfo, file_id: PathBuf, flags: OpenFlags) -> FuseResult<(OwnedFileHandle, FUSEOpenResponseFlags)> {
        if self.read_only && flags.intersects(OpenFlags::WRITE_ONLY | OpenFlags::READ_WRITE) {
            return Err(PosixError::new(libc::EROFS, "Read-only filesystem"));
        }

        if flags.contains(OpenFlags::TRUNCATE) {
            let (parent, name) = Self::file_parent_and_name(&file_id)?;
            let parent_dir = self.path_to_dir(&parent)?;
            let mut file = parent_dir
                .open_file(name)
                .map_err(|_| PosixError::new(libc::ENOENT, "File not found"))?;
            file.seek(SeekFrom::Start(0))
                .map_err(|_| PosixError::new(libc::EIO, "Seek failed"))?;
            file.truncate()
                .map_err(|_| PosixError::new(libc::EIO, "Truncate failed"))?;
        }

        let handle = self.allocate_handle();
        self.open_files.borrow_mut().insert(handle);

        Ok((
            unsafe { OwnedFileHandle::from_raw(handle) },
            FUSEOpenResponseFlags::empty(),
        ))
    }

    fn read(&self, _req: &RequestInfo, file_id: PathBuf, _file_handle: BorrowedFileHandle<'_>, seek: SeekFrom, size: u32, _flags: FUSEOpenFlags, _lock_owner: Option<u64>) -> FuseResult<Vec<u8>> {
        if !self.open_files.borrow().contains(&_file_handle.as_raw()) {
            return Err(PosixError::new(libc::EBADF, "Bad file descriptor"));
        }

        let parent = file_id
            .parent()
            .ok_or_else(|| PosixError::new(libc::EINVAL, "No parent"))?
            .to_path_buf();
        let name = file_id
            .file_name()
            .ok_or_else(|| PosixError::new(libc::EINVAL, "No filename"))?;
        let name_str = name
            .to_str()
            .ok_or_else(|| PosixError::new(libc::EINVAL, "Invalid filename"))?;

        let parent_dir = self.path_to_dir(&parent)?;
        let mut file = parent_dir
            .open_file(name_str)
            .map_err(|_| PosixError::new(libc::ENOENT, "File not found"))?;

        file.seek(seek)
            .map_err(|_| PosixError::new(libc::EIO, "Seek failed"))?;

        let mut buffer = vec![0u8; size as usize];
        let mut total_read = 0usize;
        while total_read < buffer.len() {
            let bytes_read = file
                .read(&mut buffer[total_read..])
                .map_err(|_| PosixError::new(libc::EIO, "Read failed"))?;
            if bytes_read == 0 {
                break;
            }
            total_read += bytes_read;
        }
        buffer.truncate(total_read);

        Ok(buffer)
    }

    fn write(&self, _req: &RequestInfo, file_id: PathBuf, _file_handle: BorrowedFileHandle<'_>, seek: SeekFrom, data: Vec<u8>, _write_flags: FUSEWriteFlags, _flags: OpenFlags, _lock_owner: Option<u64>) -> FuseResult<u32> {
        if self.read_only {
            return Err(PosixError::new(libc::EROFS, "Read-only filesystem"));
        }

        if !self.open_files.borrow().contains(&_file_handle.as_raw()) {
            return Err(PosixError::new(libc::EBADF, "Bad file descriptor"));
        }

        let parent = file_id
            .parent()
            .ok_or_else(|| PosixError::new(libc::EINVAL, "No parent"))?
            .to_path_buf();
        let name = file_id
            .file_name()
            .ok_or_else(|| PosixError::new(libc::EINVAL, "No filename"))?;
        let name_str = name
            .to_str()
            .ok_or_else(|| PosixError::new(libc::EINVAL, "Invalid filename"))?;

        let parent_dir = self.path_to_dir(&parent)?;
        let mut file = parent_dir
            .open_file(name_str)
            .map_err(|_| PosixError::new(libc::ENOENT, "File not found"))?;

        file.seek(seek)
            .map_err(|_| PosixError::new(libc::EIO, "Seek failed"))?;

        let mut total_written = 0usize;
        while total_written < data.len() {
            let bytes_written = file
                .write(&data[total_written..])
                .map_err(|_| PosixError::new(libc::EIO, "Write failed"))?;
            if bytes_written == 0 {
                break;
            }
            total_written += bytes_written;
        }

        Ok(total_written as u32)
    }

    fn release(&self, _req: &RequestInfo, _file_id: PathBuf, file_handle: OwnedFileHandle, _flags: OpenFlags, _lock_owner: Option<u64>, _flush: bool) -> FuseResult<()> {
        self.open_files
            .borrow_mut()
            .remove(&file_handle.borrow().as_raw());
        Ok(())
    }

    fn flush(&self, _req: &RequestInfo, _file_id: PathBuf, _file_handle: BorrowedFileHandle<'_>, _lock_owner: u64) -> FuseResult<()> {
        Ok(())
    }

    fn fsync(&self, _req: &RequestInfo, _file_id: PathBuf, _file_handle: BorrowedFileHandle<'_>, _datasync: bool) -> FuseResult<()> {
        Ok(())
    }

    fn create(&self, _req: &RequestInfo, parent: PathBuf, name: &OsStr, _mode: u32, _umask: u32, _flags: OpenFlags) -> FuseResult<(OwnedFileHandle, FileAttribute, FUSEOpenResponseFlags)> {
        if self.read_only {
            return Err(PosixError::new(libc::EROFS, "Read-only filesystem"));
        }

        let name_str = name
            .to_str()
            .ok_or_else(|| PosixError::new(libc::EINVAL, "Invalid name"))?;
        let parent_dir = self.path_to_dir(&parent)?;

        let mut file = parent_dir
            .create_file(name_str)
            .map_err(|_| PosixError::new(libc::EEXIST, "File exists"))?;

        if _flags.contains(OpenFlags::TRUNCATE) {
            file.seek(SeekFrom::Start(0))
                .map_err(|_| PosixError::new(libc::EIO, "Seek failed"))?;
            file.truncate()
                .map_err(|_| PosixError::new(libc::EIO, "Truncate failed"))?;
        }

        let handle = self.allocate_handle();
        self.open_files.borrow_mut().insert(handle);

        let attr = self.lookup(_req, parent, name)?;
        Ok((
            unsafe { OwnedFileHandle::from_raw(handle) },
            attr,
            FUSEOpenResponseFlags::empty(),
        ))
    }

    fn mkdir(&self, _req: &RequestInfo, parent: PathBuf, name: &OsStr, _mode: u32, _umask: u32) -> FuseResult<FileAttribute> {
        if self.read_only {
            return Err(PosixError::new(libc::EROFS, "Read-only filesystem"));
        }

        let name_str = name
            .to_str()
            .ok_or_else(|| PosixError::new(libc::EINVAL, "Invalid name"))?;
        let parent_dir = self.path_to_dir(&parent)?;

        parent_dir
            .create_dir(name_str)
            .map_err(|_| PosixError::new(libc::EEXIST, "Directory exists"))?;

        let attr = self.lookup(_req, parent, name)?;
        Ok(attr)
    }

    fn unlink(&self, _req: &RequestInfo, parent: PathBuf, name: &OsStr) -> FuseResult<()> {
        if self.read_only {
            return Err(PosixError::new(libc::EROFS, "Read-only filesystem"));
        }

        let name_str = name
            .to_str()
            .ok_or_else(|| PosixError::new(libc::EINVAL, "Invalid name"))?;
        let parent_dir = self.path_to_dir(&parent)?;

        parent_dir
            .remove(name_str)
            .map_err(|err| match err.kind() {
                std::io::ErrorKind::NotFound => PosixError::new(libc::ENOENT, "File not found"),
                _ => PosixError::new(libc::EIO, "Remove failed"),
            })?;

        Ok(())
    }

    fn rmdir(&self, _req: &RequestInfo, parent: PathBuf, name: &OsStr) -> FuseResult<()> {
        if self.read_only {
            return Err(PosixError::new(libc::EROFS, "Read-only filesystem"));
        }

        let name_str = name
            .to_str()
            .ok_or_else(|| PosixError::new(libc::EINVAL, "Invalid name"))?;
        let parent_dir = self.path_to_dir(&parent)?;

        parent_dir.remove(name_str).map_err(|err| {
            let message = err.to_string();
            match err.kind() {
                std::io::ErrorKind::NotFound => {
                    PosixError::new(libc::ENOENT, "Directory not found")
                }
                _ if message.contains("Directory not empty") => {
                    PosixError::new(libc::ENOTEMPTY, "Directory not empty")
                }
                _ => PosixError::new(libc::EIO, "Remove directory failed"),
            }
        })?;

        Ok(())
    }

    fn rename(&self, _req: &RequestInfo, parent: PathBuf, name: &OsStr, newparent: PathBuf, newname: &OsStr, _flags: RenameFlags) -> FuseResult<()> {
        if self.read_only {
            return Err(PosixError::new(libc::EROFS, "Read-only filesystem"));
        }

        let name_str = name
            .to_str()
            .ok_or_else(|| PosixError::new(libc::EINVAL, "Invalid source name"))?;
        let newname_str = newname
            .to_str()
            .ok_or_else(|| PosixError::new(libc::EINVAL, "Invalid destination name"))?;

        let parent_dir = self.path_to_dir(&parent)?;
        let newparent_dir = self.path_to_dir(&newparent)?;

        parent_dir
            .rename(name_str, &newparent_dir, newname_str)
            .map_err(|_| PosixError::new(libc::ENOENT, "Rename failed"))?;

        Ok(())
    }

    fn statfs(&self, _req: &RequestInfo, _file_id: PathBuf) -> FuseResult<StatFs> {
        let stats = self
            .fs
            .stats()
            .map_err(|_| PosixError::new(libc::EIO, "Failed to get stats"))?;

        Ok(StatFs {
            total_blocks: stats.total_clusters() as u64,
            free_blocks: stats.free_clusters() as u64,
            available_blocks: stats.free_clusters() as u64,
            total_files: 0,
            free_files: 0,
            block_size: stats.cluster_size() as u32,
            max_filename_length: 255,
            fragment_size: stats.cluster_size() as u32,
        })
    }

    fn access(&self, _req: &RequestInfo, file_id: PathBuf, mask: AccessMask) -> FuseResult<()> {
        if self.read_only && mask.contains(AccessMask::CAN_WRITE) {
            return Err(PosixError::new(libc::EROFS, "Read-only filesystem"));
        }

        if Self::is_root_path(&file_id) {
            return Ok(());
        }

        let parent = file_id
            .parent()
            .unwrap_or_else(|| Path::new("/"))
            .to_path_buf();
        let name = file_id
            .file_name()
            .ok_or_else(|| PosixError::new(libc::EINVAL, "No filename"))?;

        self.lookup(_req, parent, name)?;

        Ok(())
    }
}
