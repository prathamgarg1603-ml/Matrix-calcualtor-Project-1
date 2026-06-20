"""
Matrix Operations Calculator
=============================
A command-line tool for performing matrix operations using only NumPy.

Operations supported: addition, subtraction, multiplication, transpose,
determinant, and inverse.

Design
------
- Matrix              : wraps a NumPy array, owns input parsing/validation.
- MatrixCalculator    : stateless, pure math layer (no print/input calls).
                        Validates shape compatibility before delegating to
                        NumPy and raises a clear MatrixError on failure.
- MatrixCalculatorCLI : owns the menu loop and all I/O.
"""

from __future__ import annotations
import numpy as np


class MatrixError(Exception):
    """Raised when a matrix operation cannot be performed (bad shape, singular matrix, etc.)."""


class Matrix:
    """A validated 2D matrix backed by a NumPy array."""

    def __init__(self, data) -> None:
        self.array = np.array(data, dtype=float)
        if self.array.ndim != 2:
            raise MatrixError("A matrix must be 2-dimensional.")

    @property
    def shape(self) -> tuple[int, int]:
        return self.array.shape

    @property
    def is_square(self) -> bool:
        return self.shape[0] == self.shape[1]

    @classmethod
    def from_input(cls) -> "Matrix":
        """Prompt the user to type in a matrix row by row."""
        rows = int(input("Enter number of rows: "))
        cols = int(input("Enter number of columns: "))
        print(f"Enter {rows} row(s), each with {cols} space-separated value(s):")

        data = []
        for i in range(rows):
            row = list(map(float, input(f"Row {i + 1}: ").split()))
            if len(row) != cols:
                raise MatrixError(f"Row {i + 1} must have exactly {cols} value(s), got {len(row)}.")
            data.append(row)
        return cls(data)

    def __repr__(self) -> str:
        return str(self.array)


class MatrixCalculator:
    """Pure computation layer: takes Matrix objects, returns NumPy arrays/scalars."""

    @staticmethod
    def _check_same_shape(a: Matrix, b: Matrix, op: str) -> None:
        if a.shape != b.shape:
            raise MatrixError(f"Cannot {op}: shapes {a.shape} and {b.shape} do not match.")

    def add(self, a: Matrix, b: Matrix) -> np.ndarray:
        self._check_same_shape(a, b, "add")
        return np.add(a.array, b.array)

    def subtract(self, a: Matrix, b: Matrix) -> np.ndarray:
        self._check_same_shape(a, b, "subtract")
        return np.subtract(a.array, b.array)

    def multiply(self, a: Matrix, b: Matrix) -> np.ndarray:
        if a.shape[1] != b.shape[0]:
            raise MatrixError(
                f"Cannot multiply {a.shape} by {b.shape}: "
                f"columns of A ({a.shape[1]}) must equal rows of B ({b.shape[0]})."
            )
        return np.matmul(a.array, b.array)

    def transpose(self, a: Matrix) -> np.ndarray:
        return np.transpose(a.array)

    def determinant(self, a: Matrix) -> float:
        if not a.is_square:
            raise MatrixError(f"Determinant requires a square matrix, got {a.shape}.")
        return np.linalg.det(a.array)

    def inverse(self, a: Matrix) -> np.ndarray:
        if not a.is_square:
            raise MatrixError(f"Inverse requires a square matrix, got {a.shape}.")
        det = np.linalg.det(a.array)
        if np.isclose(det, 0):
            raise MatrixError("Matrix is singular (determinant ≈ 0); inverse does not exist.")
        return np.linalg.inv(a.array)


class MatrixCalculatorCLI:
    """Menu-driven interface that drives a MatrixCalculator. Owns all I/O."""

    MENU = """
===== MATRIX CALCULATOR =====
1. Addition
2. Subtraction
3. Multiplication
4. Transpose
5. Determinant
6. Inverse
7. Exit
"""

    BINARY_OPS = {"1": ("add", "Sum"), "2": ("subtract", "Difference"), "3": ("multiply", "Product")}
    UNARY_OPS = {"4": ("transpose", "Transpose"), "5": ("determinant", "Determinant"), "6": ("inverse", "Inverse")}

    def __init__(self) -> None:
        self.calculator = MatrixCalculator()

    def run(self) -> None:
        while True:
            print(self.MENU)
            choice = input("Choose an option: ").strip()

            if choice == "7":
                print("Goodbye!")
                break

            try:
                self._dispatch(choice)
            except MatrixError as e:
                print(f"Matrix error: {e}")
            except ValueError as e:
                print(f"Invalid input: {e}")
            except Exception as e:  # pragma: no cover - safety net
                print(f"Unexpected error: {e}")

    def _dispatch(self, choice: str) -> None:
        if choice in self.BINARY_OPS:
            method_name, label = self.BINARY_OPS[choice]
            print("\nMatrix A")
            a = Matrix.from_input()
            print("\nMatrix B")
            b = Matrix.from_input()
            result = getattr(self.calculator, method_name)(a, b)
            print(f"\n{label}:\n{result}")

        elif choice in self.UNARY_OPS:
            method_name, label = self.UNARY_OPS[choice]
            a = Matrix.from_input()
            result = getattr(self.calculator, method_name)(a)
            print(f"\n{label}:\n{result}")

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    MatrixCalculatorCLI().run()
