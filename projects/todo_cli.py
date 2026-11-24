"""Project: a to-do list you drive from the command line.

You build a small but complete tool in four steps:

    1. the model      a Task dataclass and a TodoList that adds, finishes and
                      removes tasks
    2. persistence    save the list to a JSON file and load it back
    3. commands       argparse subcommands: add, list, done, remove
    4. a session      run a sequence of command lines against a temp file,
                      as if you typed them in a terminal

Each command loads the file, changes the list, and saves it again, so the
program keeps no state between runs; the file is the only memory. That is how
many real command-line tools (git, for example) work.

Uses:
    05_control_flow        match on the chosen subcommand
    07_collections         lists, dicts, comprehensions
    09_classes             dataclasses
    11_errors              custom exceptions
    12_modules_io          json, pathlib, temp files
    17_os_and_command_line  argparse subcommands, exit codes
"""

import argparse
import json
import tempfile
from dataclasses import asdict
from dataclasses import dataclass, field
from pathlib import Path


class TodoError(Exception):
    """A problem the user can fix, such as an unknown task id."""


@dataclass
class Task:
    id: int
    title: str
    done: bool = False


@dataclass
class TodoList:
    tasks: list[Task] = field(default_factory=list)
    # Stored rather than computed from the tasks, so the id of a removed
    # task is never handed out again (old notes saying "#3" stay unambiguous).
    next_id: int = 1

    def add(self, title: str) -> Task:
        title = title.strip()
        if not title:
            raise TodoError("a task needs a title")
        task = Task(self.next_id, title)
        self.next_id += 1
        self.tasks.append(task)
        return task

    def find(self, task_id: int) -> Task:
        for task in self.tasks:
            if task.id == task_id:
                return task
        raise TodoError(f"no task with id {task_id}")

    def complete(self, task_id: int) -> Task:
        task = self.find(task_id)
        task.done = True
        return task

    def remove(self, task_id: int) -> Task:
        task = self.find(task_id)
        self.tasks.remove(task)
        return task

    def pending(self) -> list[Task]:
        return [t for t in self.tasks if not t.done]


def format_task(task: Task) -> str:
    mark = "x" if task.done else " "
    return f"[{mark}] {task.id:>2}  {task.title}"


def model_demo() -> None:
    todos = TodoList()
    todos.add("buy milk")
    todos.add("write report")
    todos.complete(1)
    for task in todos.tasks:
        print(format_task(task))
    print(f"pending: {len(todos.pending())}")
    try:
        todos.complete(42)
    except TodoError as exc:
        print(f"TodoError: {exc}")


def save(todos: TodoList, path: Path) -> None:
    data = {"next_id": todos.next_id, "tasks": [asdict(t) for t in todos.tasks]}
    # Write to a side file, then rename: a crash mid-write cannot leave a
    # half-written todo file behind.
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, indent=2))
    tmp.replace(path)


def load(path: Path) -> TodoList:
    if not path.exists():
        return TodoList()  # first run: start empty
    try:
        data = json.loads(path.read_text())
        tasks = [Task(**item) for item in data["tasks"]]
        return TodoList(tasks, data["next_id"])
    except (json.JSONDecodeError, KeyError, TypeError) as exc:
        raise TodoError(f"{path.name} is damaged: {exc}") from exc


def persistence_demo() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "todo.json"
        todos = load(path)
        print(f"fresh start: {len(todos.tasks)} tasks")
        todos.add("water plants")
        todos.complete(todos.add("call bank").id)
        save(todos, path)
        print(f"saved {path.name}: {path.read_text().count('title')} tasks")
        print(f"reloaded equal to original: {load(path) == todos}")

        path.write_text("{not json")
        try:
            load(path)
        except TodoError as exc:
            print(f"TodoError: {exc}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="todo", description="A tiny to-do list.")
    sub = parser.add_subparsers(dest="command", required=True)
    add = sub.add_parser("add", help="add a task")
    add.add_argument("title", nargs="+", help="words of the title")
    show = sub.add_parser("list", help="show tasks")
    show.add_argument("--all", action="store_true", help="include finished ones")
    for name, help_text in [("done", "mark a task finished"),
                            ("remove", "delete a task")]:
        cmd = sub.add_parser(name, help=help_text)
        cmd.add_argument("id", type=int)
    return parser


def run(argv: list[str], path: Path) -> int:
    """Run one command line; return a process exit code (0 means success)."""
    args = build_parser().parse_args(argv)
    todos = load(path)
    try:
        match args.command:
            case "add":
                task = todos.add(" ".join(args.title))
                print(f"added #{task.id}: {task.title}")
            case "list":
                shown = todos.tasks if args.all else todos.pending()
                for task in shown:
                    print(format_task(task))
                print(f"({len(todos.pending())} to do, {len(todos.tasks)} total)")
            case "done":
                print(f"finished #{todos.complete(args.id).id}")
            case "remove":
                print(f"removed: {todos.remove(args.id).title}")
    except TodoError as exc:
        print(f"error: {exc}")
        return 1
    save(todos, path)
    return 0


def commands_demo() -> None:
    print(build_parser().format_usage().strip())
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "todo.json"
        print(f"exit code {run(['add', 'learn', 'argparse'], path)}")
        print(f"exit code {run(['done', '7'], path)}")


def main() -> None:
    model_demo()
    print()
    persistence_demo()
    print()
    commands_demo()


if __name__ == "__main__":
    main()
