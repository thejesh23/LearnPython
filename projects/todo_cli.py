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

from dataclasses import dataclass, field


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


def main() -> None:
    model_demo()


if __name__ == "__main__":
    main()
