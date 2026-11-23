# euler_kit

A tiny registry of solved Project Euler problems (1, 2, 3, 7, 10, 14), each with its known answer, plus the number helpers they share.

```bash
python3 -m project_euler.euler_kit     # run and time every problem, seven examples, then a randomized self-check
```

```python
from project_euler.euler_kit import PROBLEMS, run, prime_factors

run(14).ok                       # True: the solver's value equals the accepted answer
PROBLEMS[3].solve(13195)         # 29, the worked example from the problem statement
prime_factors(360)               # [2, 2, 2, 3, 3, 5]
```

| API | Module |
|---|---|
| `PROBLEMS`, `@problem(number, title, answer)`, `run`, `run_all`, `Problem`, `Result` | `problems.py` |
| `sum_multiples`, `fibonacci_below`, `primes_below`, `is_prime`, `nth_prime`, `prime_factors`, `collatz_sequence`, `collatz_length` | `helpers.py` |

Each solver takes the problem size as an argument (the real size is the default), so the small example from each problem statement doubles as a test.
Standalone write-ups of problems 1, 2, 3 and 14 live next to this folder, e.g. `../problem_014_longest_collatz.py`.
