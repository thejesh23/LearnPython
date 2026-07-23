"""A tiny neural network trained by hand-written backpropagation on XOR.

XOR is the classic problem a single linear layer cannot solve, because the two
classes are not linearly separable. One hidden layer with a nonlinear activation
fixes that: the hidden units bend the input space until the output layer can
separate the classes with a plane. This file builds a 2-2-1 network and trains
it with plain gradient descent.

Backpropagation is the chain rule applied layer by layer. A forward pass
computes the hidden activations and the output; the loss gradient is pushed
backward, multiplying by each layer's local derivative (the sigmoid's is
a(1-a)), to get the gradient for every weight and bias. Those are nudged down
the gradient by a learning rate. With a good weight init and enough epochs the
squared-error loss falls steadily and the network learns the exact XOR truth
table, which is verified at the end.
"""

import math
import random

Vector = list[float]
Matrix = list[list[float]]


def sigmoid(x: float) -> float:
    # Split by sign to avoid overflow in exp for large-magnitude inputs.
    if x >= 0:
        return 1.0 / (1.0 + math.exp(-x))
    z = math.exp(x)
    return z / (1.0 + z)


class TinyNet:
    """A 2 -> hidden -> 1 fully-connected net with sigmoid activations."""

    def __init__(self, n_in: int, n_hidden: int, seed: int = 0) -> None:
        rng = random.Random(seed)
        # Small random weights break symmetry so hidden units learn differently.
        self.w1: Matrix = [[rng.uniform(-1, 1) for _ in range(n_in)]
                           for _ in range(n_hidden)]
        self.b1: Vector = [rng.uniform(-1, 1) for _ in range(n_hidden)]
        self.w2: Vector = [rng.uniform(-1, 1) for _ in range(n_hidden)]
        self.b2: float = rng.uniform(-1, 1)
        self.n_hidden = n_hidden

    def forward(self, x: Vector) -> tuple[Vector, float]:
        h = [sigmoid(sum(self.w1[j][k] * x[k] for k in range(len(x)))
                     + self.b1[j]) for j in range(self.n_hidden)]
        out = sigmoid(sum(self.w2[j] * h[j] for j in range(self.n_hidden))
                      + self.b2)
        return h, out

    def train(self, xs: list[Vector], ys: list[float],
              epochs: int = 5000, lr: float = 0.5) -> list[float]:
        history: list[float] = []
        for _ in range(epochs):
            loss = 0.0
            for x, y in zip(xs, ys):
                h, out = self.forward(x)
                loss += (out - y) ** 2
                # Output layer gradients (squared error * sigmoid').
                d_out = 2 * (out - y) * out * (1 - out)
                # Backprop into hidden layer.
                d_hidden = [d_out * self.w2[j] * h[j] * (1 - h[j])
                            for j in range(self.n_hidden)]
                # Update output weights and bias.
                for j in range(self.n_hidden):
                    self.w2[j] -= lr * d_out * h[j]
                self.b2 -= lr * d_out
                # Update hidden weights and biases.
                for j in range(self.n_hidden):
                    for k in range(len(x)):
                        self.w1[j][k] -= lr * d_hidden[j] * x[k]
                    self.b1[j] -= lr * d_hidden[j]
            history.append(loss / len(xs))
        return history

    def predict(self, x: Vector) -> float:
        return self.forward(x)[1]


def main() -> None:
    xs: list[Vector] = [[0.0, 0.0], [0.0, 1.0], [1.0, 0.0], [1.0, 1.0]]
    ys: list[float] = [0.0, 1.0, 1.0, 0.0]  # XOR truth table

    net = TinyNet(n_in=2, n_hidden=4, seed=1)
    history = net.train(xs, ys, epochs=5000, lr=0.5)

    print("mean-squared error during training")
    for epoch in (1, 100, 500, 1000, 2500, 5000):
        print(f"  epoch {epoch:>5}: MSE {history[epoch - 1]:.6f}")
    print(f"\nloss decreased: {history[-1] < history[0]}")

    print("\nlearned XOR function (input -> output, rounds to target)")
    correct = 0
    for x, y in zip(xs, ys):
        out = net.predict(x)
        rounded = round(out)
        correct += rounded == y
        print(f"  {x} -> {out:.4f}  (rounds to {rounded}, target {int(y)})")
    print(f"\nall four rows correct: {correct == 4}")

    # A single linear unit (no hidden layer) provably cannot fit XOR.
    linear = TinyNet(n_in=2, n_hidden=1, seed=2)
    lin_hist = linear.train(xs, ys, epochs=5000, lr=0.5)
    print(f"\none hidden unit is too small: final MSE {lin_hist[-1]:.4f} "
          f"(stays high, cannot separate XOR)")


if __name__ == "__main__":
    main()
