# Exercises

Practice for every chapter of the course in [`basics/`](../basics/): 121 exercises
across 22 files, from warm-ups to small puzzles.

## How it works

Each file is a list of tasks. Every task is a function (or class) with a
docstring that says what to build, and a body that just raises
`NotImplementedError`. Below each one is a test that checks your answer.

1. Run the file. Every line starts as `[todo] not attempted`:

   ```bash
   python3 exercises/ch01_variables.py
   ```

2. Replace a `raise NotImplementedError` with your code and run it again.
   - `[solved]` means the tests pass.
   - `[not yet] ...` tells you which case failed, and what came back.
3. Keep going until every line says `[solved]`.

The tests never crash the file, so you can solve the exercises in any order.
When you are stuck, the matching file in [`solutions/`](solutions/) has an
idiomatic answer with comments. It runs the *same* tests, so
`python3 exercises/solutions/ch01_variables.py` prints all `[solved]`.

Tip: copy the folder (or use `git stash` afterwards) if you want to keep the
original stubs to retry later.

## The exercises

| Ch | Exercises | Solution | Lesson | Tasks |
|----|-----------|----------|--------|-------|
| 01 | [`ch01_variables.py`](ch01_variables.py) | [solution](solutions/ch01_variables.py) | [lesson](../basics/01_variables/) | `swap`, `rotate_left`, `ends`, `head_and_tail`, `life_summary` |
| 02 | [`ch02_types.py`](ch02_types.py) | [solution](solutions/ch02_types.py) | [lesson](../basics/02_types/) | `utf8_length`, `split_seconds`, `simplify`, `add_money`, `describe`, `to_int` |
| 03 | [`ch03_operators.py`](ch03_operators.py) | [solution](solutions/ch03_operators.py) | [lesson](../basics/03_operators/) | `is_even`, `in_range`, `display_name`, `is_vowel`, `is_leap_year`, `ceil_div` |
| 04 | [`ch04_strings.py`](ch04_strings.py) | [solution](solutions/ch04_strings.py) | [lesson](../basics/04_strings/) | `format_price`, `initials`, `is_palindrome`, `mask_card`, `parse_setting` |
| 05 | [`ch05_control_flow.py`](ch05_control_flow.py) | [solution](solutions/ch05_control_flow.py) | [lesson](../basics/05_control_flow/) | `fizzbuzz`, `sum_of_multiples`, `first_index`, `collatz_steps`, `is_prime`, `parse_command` |
| 06 | [`ch06_functions.py`](ch06_functions.py) | [solution](solutions/ch06_functions.py) | [lesson](../basics/06_functions/) | `average`, `make_greeting`, `append_to`, `by_last_name`, `make_accumulator`, `uppercase_result` |
| 07 | [`ch07_collections.py`](ch07_collections.py) | [solution](solutions/ch07_collections.py) | [lesson](../basics/07_collections/) | `squares_of_evens`, `unique_in_order`, `word_counts`, `group_by_length`, `common_items`, `top_scorers` |
| 08 | [`ch08_iterators.py`](ch08_iterators.py) | [solution](solutions/ch08_iterators.py) | [lesson](../basics/08_iterators/) | `first_or_default`, `countdown`, `running_total`, `chunks`, `run_lengths`, `interleave` |
| 09 | [`ch09_classes.py`](ch09_classes.py) | [solution](solutions/ch09_classes.py) | [lesson](../basics/09_classes/) | `Rectangle`, `BankAccount`, `Vector`, `Version.from_string`, `Manager(Employee)` |
| 10 | [`ch10_async.py`](ch10_async.py) | [solution](solutions/ch10_async.py) | [lesson](../basics/10_async/) | `add_later`, `fetch_all`, `with_timeout`, `countdown`, `bounded_map` |
| 11 | [`ch11_errors.py`](ch11_errors.py) | [solution](solutions/ch11_errors.py) | [lesson](../basics/11_errors/) | `safe_int`, `parse_age`, `InsufficientFunds`, `retry`, `validate_order`, `split_errors` |
| 12 | [`ch12_modules_io.py`](ch12_modules_io.py) | [solution](solutions/ch12_modules_io.py) | [lesson](../basics/12_modules_io/) | `count_lines`, `write_scores`, `load_settings`, `csv_totals`, `load_module`, `atomic_write` |
| 13 | [`ch13_standard_library.py`](ch13_standard_library.py) | [solution](solutions/ch13_standard_library.py) | [lesson](../basics/13_standard_library/) | `top_words`, `group_by_length`, `moving_average`, `add_business_days`, `us_to_iso`, `count_paths` |
| 14 | [`ch14_testing.py`](ch14_testing.py) | [solution](solutions/ch14_testing.py) | [lesson](../basics/14_testing/) | `check_is_leap`, `assert_raises`, `check_send_welcome`, `greeting_at`, `StackTests` |
| 15 | [`ch15_typing.py`](ch15_typing.py) | [solution](solutions/ch15_typing.py) | [lesson](../basics/15_typing/) | `first[T]`, `parse_mode`, `double with @overload`, `compose[A, B, C]`, `Registry[T]`, `type_errors` |
| 16 | [`ch16_threads_and_processes.py`](ch16_threads_and_processes.py) | [solution](solutions/ch16_threads_and_processes.py) | [lesson](../basics/16_threads_and_processes/) | `parallel_map`, `SafeCounter`, `run_all`, `fastest`, `process_queue`, `primes_in_processes` |
| 17 | [`ch17_os_and_command_line.py`](ch17_os_and_command_line.py) | [solution](solutions/ch17_os_and_command_line.py) | [lesson](../basics/17_os_and_command_line/) | `env_settings`, `build_parser`, `find_files`, `run_python`, `linecount` |
| 18 | [`ch18_data_and_storage.py`](ch18_data_and_storage.py) | [solution](solutions/ch18_data_and_storage.py) | [lesson](../basics/18_data_and_storage/) | `sha256_file`, `parse_header`, `add_user`, `top_customers`, `safe_extract` |
| 19 | [`ch19_networking.py`](ch19_networking.py) | [solution](solutions/ch19_networking.py) | [lesson](../basics/19_networking/) | `get_param`, `add_params`, `send_and_receive`, `handle_lines`, `fetch_json` |
| 20 | [`ch20_performance.py`](ch20_performance.py) | [solution](solutions/ch20_performance.py) | [lesson](../basics/20_performance/) | `has_duplicates`, `common_words`, `parse_readings`, `memoize`, `most_called` |
| 21 | [`ch21_pythonic_code.py`](ch21_pythonic_code.py) | [solution](solutions/ch21_pythonic_code.py) | [lesson](../basics/21_pythonic_code/) | `scoreboard`, `remove_short`, `make_multipliers`, `load_port`, `get_nested` |
| 22 | [`ch22_packaging_and_projects.py`](ch22_packaging_and_projects.py) | [solution](solutions/ch22_packaging_and_projects.py) | [lesson](../basics/22_packaging_and_projects/) | `bump_version`, `parse_requirement`, `read_project`, `load_entry_point`, `run_tests` |
