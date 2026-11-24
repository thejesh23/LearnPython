"""Working with whole folders: finding, walking, copying, moving and deleting.

`pathlib` (see 12_modules_io/files_and_pathlib.py) reads and writes single
files. This file is about trees of files, the jobs a shell script would do:

    Path.glob / rglob    find files by pattern, here or in every subfolder
    os.walk              visit every folder, choosing which ones to skip
    shutil.copy2         copy one file, keeping its timestamps
    shutil.copytree      copy a whole folder
    shutil.move          move or rename, even across drives
    shutil.rmtree        delete a folder and everything in it
    tempfile             scratch files and folders that clean themselves up
    shutil.disk_usage    how much space a drive has left

`rmtree` and `move` do not ask for confirmation and there is no recycle bin.
Everything below happens inside a TemporaryDirectory, which is deleted at
the end of its `with` block.
"""

import os
import shutil
import tempfile
from pathlib import Path


def make_project(root: Path) -> None:
    """Create a small, fake project to play with."""
    files = {
        "README.md": "# demo\n",
        "src/app.py": "print('app')\n",
        "src/utils.py": "def helper(): ...\n",
        "src/data/cities.csv": "name\nLisbon\n",
        "tests/test_app.py": "def test(): ...\n",
        ".cache/old.py": "# generated\n",
    }
    for name, text in files.items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")


def show(paths: list[Path], root: Path) -> list[str]:
    # Paths relative to root and sorted, so the output does not depend on
    # where the temp folder is or on the order the OS returns files in.
    return sorted(p.relative_to(root).as_posix() for p in paths)


def glob_demo() -> None:
    with tempfile.TemporaryDirectory() as folder:
        root = Path(folder)
        make_project(root)
        # glob matches in one folder; '*' is any run of characters.
        print(f"glob('*.md'):       {show(list(root.glob('*.md')), root)}")
        print(f"glob('src/*.py'):   {show(list(root.glob('src/*.py')), root)}")
        # rglob (or glob('**/...')) searches every subfolder, hidden ones too.
        print(f"rglob('*.py'):      {show(list(root.rglob('*.py')), root)}")
        print(f"rglob('test_*.py'): {show(list(root.rglob('test_*.py')), root)}")
        folders = [p for p in root.iterdir() if p.is_dir()]
        print(f"iterdir() folders:  {show(folders, root)}")


def walk_demo() -> None:
    with tempfile.TemporaryDirectory() as folder:
        root = Path(folder)
        make_project(root)
        total = 0
        # os.walk yields (folder, its subfolder names, its file names) for
        # every folder, starting at the top.
        for dirpath, dirnames, filenames in os.walk(root):
            # Editing dirnames in place tells walk which folders to enter.
            # This is how tools skip .git, .cache or node_modules.
            dirnames[:] = sorted(d for d in dirnames if not d.startswith("."))
            here = Path(dirpath).relative_to(root).as_posix()
            size = sum((Path(dirpath) / f).stat().st_size for f in filenames)
            total += size
            print(f"  {here:<10} {len(filenames)} file(s), {size:>3} bytes")
        print(f"total without hidden folders: {total} bytes")


def copy_move_delete_demo() -> None:
    with tempfile.TemporaryDirectory() as folder:
        root = Path(folder)
        make_project(root)

        # copy2 copies contents and timestamps; the target may be a folder.
        backup = root / "backup"
        backup.mkdir()
        shutil.copy2(root / "README.md", backup)
        print(f"after copy2: {show(list(backup.iterdir()), root)}")

        # copytree copies a whole folder; ignore= leaves some files out.
        shutil.copytree(root / "src", backup / "src",
                        ignore=shutil.ignore_patterns("*.csv"))
        print(f"after copytree: {show(list(backup.rglob('*.*')), root)}")

        # move renames when it can, or copies then deletes when it must.
        shutil.move(root / "tests", root / "checks")
        print(f"tests/ renamed: {(root / 'checks').exists()}, "
              f"old name gone: {not (root / 'tests').exists()}")

        # rmtree deletes a folder and everything inside it, without asking.
        shutil.rmtree(backup)
        print(f"backup removed: {not backup.exists()}")

        # Path.rmdir only removes an empty folder, which makes it the safer choice.
        try:
            (root / "src").rmdir()
        except OSError:
            print("Path.rmdir on a non-empty folder -> OSError")


def human(size: float) -> str:
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} PB"


def tempfile_and_disk_demo() -> None:
    # NamedTemporaryFile: a real file with a path, deleted when closed.
    with tempfile.NamedTemporaryFile("w+", suffix=".txt", encoding="utf-8") as f:
        f.write("scratch data")
        f.seek(0)
        print(f"the {Path(f.name).suffix} temp file holds: {f.read()!r}")
    print(f"deleted after the block: {not Path(f.name).exists()}")

    # The temp folder is chosen by the OS (TMPDIR, TEMP or a default).
    print(f"gettempdir() exists: {Path(tempfile.gettempdir()).is_dir()}")

    with tempfile.TemporaryDirectory(prefix="learnpy-") as folder:
        print(f"TemporaryDirectory name starts with: {Path(folder).name[:8]}")

        # disk_usage reports the drive that holds the given path.
        usage = shutil.disk_usage(folder)
        print(f"that drive: {human(usage.total)} total, "
              f"{usage.used / usage.total:.0%} used")
        print(f"room for a 100 MB download: {usage.free > 100 * 1024**2}")
    print(f"human(1536) = {human(1536)}, human(5 * 1024**3) = {human(5 * 1024**3)}")


def main() -> None:
    glob_demo()
    print()
    walk_demo()
    print()
    copy_move_delete_demo()
    print()
    tempfile_and_disk_demo()


if __name__ == "__main__":
    main()
