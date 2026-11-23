# numeric_kit

Numerical methods on plain floats and lists: derivatives, root finding, integration, ODEs and small dense linear systems.

```bash
python3 -m numeric.numeric_kit     # six examples plus a randomized self-check
```

```python
import math
from numeric.numeric_kit import bisect_root, integrate, solve

bisect_root(lambda x: x * x - 2, 0, 2)     # 1.41421356...
integrate(math.sin, 0, math.pi)            # 2.0 (to ~1e-10)
solve([[2, 1], [1, 3]], [3, 5])            # [0.8, 1.4]
```

| Function | Module | Teaches |
|---|---|---|
| `derivative` | `calculus.py` | central differences |
| `bisect_root`, `newton_root` | `calculus.py` | safe-but-slow bracketing vs fast tangent steps |
| `integrate` | `calculus.py` | adaptive Simpson with an error estimate |
| `rk4` | `calculus.py` | fourth-order Runge-Kutta for `y' = f(t, y)` |
| `solve`, `determinant` | `linalg.py` | Gaussian elimination with partial pivoting |
| `dominant_eigen`, `mat_vec` | `linalg.py` | power iteration and the Rayleigh quotient |

Answers are approximate, so the self-check compares with `math.isclose` against closed forms and brute force.
Standalone versions live next to this folder, e.g. `../newton_raphson.py`.
