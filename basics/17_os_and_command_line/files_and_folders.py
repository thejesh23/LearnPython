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


def main() -> None:
    glob_demo()


if __name__ == "__main__":
    main()
