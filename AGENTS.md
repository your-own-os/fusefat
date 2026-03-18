# AI Development Tips

This document provides guidance for AI agents working on this project.

## Dependency Management

When updating dependencies:
1. Check available versions: `cargo search <package>`
2. Update Cargo.toml with new versions
3. Run `cargo update`
4. Fix any API breaking changes

## Important Notes

1. **No sudo in test code**: Tests should run as non-root. The conftest.py uses `sudo` internally for mounting, but tests don't need sudo.

2. **FAT image creation**: Images must be created separately using `mkimages` before running tests.

3. **Loop device mounting**: Tests mount FAT images via loop devices using kernel's FAT driver to verify filesystem behavior.

## Code Style

- Rust: Follow existing conventions, use `cargo fmt` before committing
- Python: Follow PEP 8, use meaningful variable names, but:
  - keep function definitions in one line

## Other

- Delete __pycache__ directories after running tests
