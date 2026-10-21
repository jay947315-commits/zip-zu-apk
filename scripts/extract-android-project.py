#!/usr/bin/env python3
import stat
import sys
import zipfile
from pathlib import Path, PurePosixPath

MAX_FILES = 50_000
MAX_UNCOMPRESSED_SIZE = 2 * 1024 * 1024 * 1024


def fail(message):
    print(f"Error: {message}", file=sys.stderr)
    raise SystemExit(1)


def main():
    if len(sys.argv) != 3:
        fail("Usage: extract-android-project.py ZIP_PATH DESTINATION")

    archive_path = Path(sys.argv[1])
    destination = Path(sys.argv[2]).resolve()
    if not archive_path.is_file():
        fail(f"ZIP file not found: {archive_path}")

    destination.mkdir(parents=True, exist_ok=True)

    try:
        with zipfile.ZipFile(archive_path) as archive:
            entries = archive.infolist()
            if len(entries) > MAX_FILES:
                fail(f"Archive contains more than {MAX_FILES} entries")

            total_size = sum(entry.file_size for entry in entries)
            if total_size > MAX_UNCOMPRESSED_SIZE:
                fail("Archive expands to more than 2 GiB")

            for entry in entries:
                member = PurePosixPath(entry.filename)
                mode = entry.external_attr >> 16
                if (
                    member.is_absolute()
                    or ".." in member.parts
                    or stat.S_ISLNK(mode)
                ):
                    fail(f"Unsafe ZIP entry: {entry.filename}")

                target = (destination / Path(*member.parts)).resolve()
                if target != destination and destination not in target.parents:
                    fail(f"ZIP entry escapes destination: {entry.filename}")

                if entry.is_dir():
                    target.mkdir(parents=True, exist_ok=True)
                    continue

                target.parent.mkdir(parents=True, exist_ok=True)
                with archive.open(entry) as source, target.open("wb") as output:
                    while chunk := source.read(1024 * 1024):
                        output.write(chunk)

    except (OSError, zipfile.BadZipFile, RuntimeError) as error:
        fail(f"Could not extract ZIP: {error}")

    wrappers = list(destination.rglob("gradlew"))
    if len(wrappers) != 1:
        fail(
            "Expected exactly one Gradle wrapper (gradlew) in the archive; "
            f"found {len(wrappers)}"
        )

    wrapper = wrappers[0]
    if not wrapper.is_file():
        fail(f"Gradle wrapper is not a regular file: {wrapper}")

    wrapper.chmod(wrapper.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    print(f"Android project extracted to {wrapper.parent}")


if __name__ == "__main__":
    main()
