# Matrix Operations Calculator

A small, dependency-light CLI tool for performing common matrix operations, built entirely on top of NumPy — no other libraries used.

## Features
- Addition
- Subtraction
- Multiplication
- Transpose
- Determinant
- Inverse

## Design

The code is split into three classes, each with a single responsibility:

| Class | Responsibility |
|---|---|
| `Matrix` | Wraps a NumPy array. Owns input parsing and validation (correct row length, 2D shape). |
| `MatrixCalculator` | Pure math layer — no `print`/`input` calls. Validates shape compatibility *before* calling NumPy and raises a clear `MatrixError` instead of letting a raw NumPy exception leak through. |
| `MatrixCalculatorCLI` | Owns the menu loop and all I/O, and dispatches to `MatrixCalculator`. |

Keeping I/O out of `MatrixCalculator` means the math logic is reusable/testable independent of the command line (e.g. you could drop it into a web backend later without touching it).

## Requirements
- Python 3.8+
- NumPy

```bash
pip install numpy
```

## Usage

```bash
python matrix_calculator.py
```

You'll see a menu:

```
===== MATRIX CALCULATOR =====
1. Addition
2. Subtraction
3. Multiplication
4. Transpose
5. Determinant
6. Inverse
7. Exit
```

### Example — Addition

```
Choose an option: 1

Matrix A
Enter number of rows: 2
Enter number of columns: 2
Enter 2 row(s), each with 2 space-separated value(s):
Row 1: 1 2
Row 2: 3 4

Matrix B
Enter number of rows: 2
Enter number of columns: 2
Row 1: 5 6
Row 2: 7 8

Sum:
[[ 6.  8.]
 [10. 12.]]
```

### Example — Determinant

```
Choose an option: 5
Enter number of rows: 2
Enter number of columns: 2
Row 1: 4 7
Row 2: 2 6

Determinant:
10.000000000000002
```

### Example — Multiplication (incompatible shapes)

```
Choose an option: 3

Matrix A
Enter number of rows: 2
Enter number of columns: 3
Row 1: 1 2 3
Row 2: 4 5 6

Matrix B
Enter number of rows: 2
Enter number of columns: 2
Row 1: 1 0
Row 2: 0 1

Matrix error: Cannot multiply (2, 3) by (2, 2): columns of A (3) must equal rows of B (2).
```

### Example — Inverse of a singular matrix

```
Choose an option: 6
Enter number of rows: 2
Enter number of columns: 2
Row 1: 2 4
Row 2: 1 2

Matrix error: Matrix is singular (determinant ≈ 0); inverse does not exist.
```

## Project structure

```
.
├── matrix_calculator.py
└── README.md
```

## Possible extensions
- Unit tests with `pytest` for `MatrixCalculator` (no I/O to mock, since it's pure).
- Support reading matrices from a `.csv` file instead of stdin.
- Scalar multiplication and matrix power (`np.linalg.matrix_power`).
