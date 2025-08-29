# Symbolic Math CLI Tool

A powerful, feature-rich command-line tool for symbolic mathematics, built in Python using the SymPy library. It can be used as an interactive calculator (REPL) or to evaluate scripts from a file.

## Features

*   **Interactive REPL & File Evaluation:** Use it on the fly or run pre-written scripts.
*   **Stateful Memory:** Define and delete variables and constants that persist within a session.
*   **Symbolic Mathematics:** It's not just a calculator; it understands symbolic expressions.
*   **Calculus & Algebra:** Perform differentiation, integration, and solve equations.
*   **Flexible Syntax:** Supports multi-statement lines, quiet mode for assignments, and formatted numbers.
*   **Arbitrary & Default Precision:** Evaluate expressions to any number of decimal places, with a sensible default.
*   **Rich Function Library:** Includes a wide range of trigonometric, logarithmic, and root functions.

## Setup

To use this tool, first install the necessary dependencies:

```bash
pip install -r requirements.txt
```

## Usage

There are two ways to use the tool:

### 1. Interactive REPL

For a quick, line-by-line calculator, run the `math_cli.py` script:

```bash
python3 math_cli.py
```

This will open a prompt where you can enter expressions. Type `quit` or `exit` to leave.

**Example Session:**
```
> x = 10, y = 20 --q
> diff y * x**3 + sin(x) wrt x
3*x**2*y + cos(x)
> pi
3.14159
> del x, y
Deleted: x, y
```

### 2. File Evaluator

For running a script of commands, use the `math_file_eval.py` script, passing the path to your file:

```bash
python3 math_file_eval.py path/to/your/script.txt
```

The script file should contain one command per line. Lines starting with `#` are treated as comments and are ignored.

**Example `script.txt`:**
```
# Define some variables and constants
a = 5, const G = 9.8 --q

# Perform a calculation
result = a * G
result

# Display the final state
disp
```

**Corresponding Output:**
```
In:  result = a * G
Out: Defined variable result = 49.0

In:  result
Out: 49.0

In:  disp
Out:
Built-Ins:
  e = 2.71828
  pi = 3.14159
  tau = 6.28319

Constants:
  G = 9.8

Variables:
  a = 5
  result = 49.0
```

## Commands & Syntax Reference

### General Syntax

*   **Multi-Statement Lines:** You can enter multiple commands on one line, separated by commas.
    ```
    x = 10, const C = 5, x * C
    ```
*   **Quiet Mode:** To suppress the confirmation output for assignments, end the line with `--q`.
    ```
    my_var = 12345 --q
    ```
*   **Number Formatting:** You can use commas in numbers for readability. They will be ignored during evaluation.
    ```
    1,000,000 / 2
    ```

### Variable Assignment

Use the `=` operator. Variables can be reassigned. The confirmation message will show the evaluated result.
```
> my_var = 10 * 5
Defined variable my_var = 50
```

### Constant Assignment

Use the `const` keyword. Constants cannot be reassigned once defined.
```
> const SPEED_OF_LIGHT = 299,792,458
Defined constant SPEED_OF_LIGHT = 299792458
```

### Deletion

*   Use the `del` keyword to delete one or more variables or constants.
*   You cannot delete the built-in constants (`pi`, `e`, `tau`).
```
del my_var, SPEED_OF_LIGHT
```

### Display Commands

*   `disp`: Shows all defined items, categorized into `Built-Ins`, `Constants`, and `Variables`.
*   `disp vars`: Shows only user-defined variables.
*   `disp consts`: Shows only user-defined constants.

**Example `disp` output:**
```
Built-Ins:
  e = 2.71828
  pi = 3.14159
  tau = 6.28319

Constants:
  (none)

Variables:
  x = 10
```

### Precision

*   **Default Precision:** All numerical results are formatted to a default precision (5 decimal places, where applicable). Trailing zeros are removed.
*   **Arbitrary Precision:** Use the `to N places` syntax at the end of an expression to evaluate it numerically to a specific precision.
    ```
    > 1/7
    0.142857
    > 1/7 to 20 places
    0.14285714285714285714
    ```

### Supported Functions

The tool supports a wide range of common mathematical functions.

*   **Trigonometric:** `sin`, `cos`, `tan`, `csc`, `sec`, `cot`
*   **Inverse Trig:** `asin`, `acos`, `atan`, etc.
*   **Roots:** `sqrt(x)`, `cbrt(x)`, `root(x, n)`
*   **Logarithms:** `log(x, base)`, `ln(x)`

---

### Calculus and Solving

#### `diff` - Differentiation

Calculates the derivative of an expression.

**Syntax:** `diff <expression> [wrt <variable>]`

*   If the expression contains only one variable, you can omit `wrt`.
*   If the expression contains multiple variables, you must specify which one to differentiate with respect to.

**Examples:**
```
> diff x**3 + 2*x
2*x + 3*x**2

> a=5, b=10 --q
> diff a*x**2 + b*y wrt x
10*x
```

#### `int` - Integration

Calculates the definite or indefinite integral of an expression.

**Syntax (Indefinite):** `int <expression> [wrt <variable>]`
**Syntax (Definite):** `int <expression> [wrt <variable>] from <a> to <b>`

*   The `wrt` clause is optional if the expression contains only one variable.
*   For definite integrals, the `wrt` clause can come before or after the `from...to` clause.
*   Indefinite integrals will include the constant of integration, `C`.

**Examples:**
```
> int x**2 + x
C + x**2/2 + x**3/3

> int x*y wrt x
C + x**2*y/2

> int x from 0 to 1
1/2

> int x*y from 0 to 1 wrt x
y/2
```

#### `solve` - Equation Solving

Solves an equation for a given variable.

**Syntax:** `solve <equation> [wrt <variable>]`

*   Equations can be written with an `=` sign (e.g., `x**2 = 4`) or as an expression that is assumed to equal zero (e.g., `x**2 - 4`).
*   Like `diff`, the variable is optional if it is unambiguous.

**Examples:**
```
> solve x**2 - 9
Solutions: x = -3, 3

> solve a*x = b wrt x
Solutions: x = b/a
```
