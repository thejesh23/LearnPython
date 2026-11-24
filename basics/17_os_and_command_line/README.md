# 17 · The OS and the command line

Arguments, environment, running other programs, files and exit codes.

Read the files in this order; each one runs on its own:

| # | File | What it teaches |
|---|------|-----------------|
| 1 | [`command_line_arguments.py`](command_line_arguments.py) | Reading command-line arguments: `sys.argv` by hand, then `argparse`. |
| 2 | [`environment_and_platform.py`](environment_and_platform.py) | Environment variables, the running Python, the current directory and PATH. |
| 3 | [`files_and_folders.py`](files_and_folders.py) | Working with whole folders: finding, walking, copying, moving and deleting. |
| 4 | [`running_programs.py`](running_programs.py) | Running other programs from Python with `subprocess.run`. |
| 5 | [`exit_codes_and_cleanup.py`](exit_codes_and_cleanup.py) | How a program ends: exit codes, stdout vs stderr, cleanup and signals. |

```bash
python3 basics/17_os_and_command_line/command_line_arguments.py
```

## Practice

Open [`exercises/ch17_os_and_command_line.py`](../../exercises/ch17_os_and_command_line.py), fill in each function, and run the file until every line says `[solved]`. Stuck? Compare with [`exercises/solutions/ch17_os_and_command_line.py`](../../exercises/solutions/ch17_os_and_command_line.py).

## Going deeper

- [`advanced/argparse_cli.py`](../../advanced/argparse_cli.py)
- [`advanced/subprocess_and_processes.py`](../../advanced/subprocess_and_processes.py)

---

← [16_threads_and_processes](../16_threads_and_processes/) · [18_data_and_storage](../18_data_and_storage/) →
