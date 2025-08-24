# Symbolic Math CLI Tool

A powerful, feature-rich command-line tool for symbolic mathematics, built in Python using the SymPy library. It can be used as an interactive calculator (REPL) or to evaluate scripts from a file.

## Features

*   **Interactive REPL & File Evaluation:** Use it on the fly or run pre-written scripts.
*   **Stateful Memory:** Define variables and constants that persist within a session.
*   **Symbolic Mathematics:** It's not just a calculator; it understands symbolic expressions.
*   **Calculus & Algebra:** Perform differentiation, integration, and solve equations.
*   **Arbitrary Precision:** Evaluate expressions to any number of decimal places.
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
> x = 10
Defined variable x
> diff(x**3 + sin(x), x)
3*x**2 + cos(x)
> pi to 20 places
3.14159265358979323846
> quit
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
a = 5
const G = 9.8

# Perform a calculation
result = a * G
result

# Display the final state
disp
```

**Output:**
```
In:  a = 5
Out: Defined variable a

In:  const G = 9.8
Out: Defined constant G

In:  result = a * G
Out: Defined variable result

In:  result
Out: 49.0000000000000

In:  disp
Out:
Constants:
  G = 9.80000000000000
  e = E
  pi = pi
  tau = 2*pi

Variables:
  a = 5
  result = 49.0000000000000
```


## Commands & Syntax Reference

### Variable Assignment

Use the `=` operator. Variables can be reassigned.

```
my_var = 10 * 5
```

### Constant Assignment

Use the `const` keyword. Constants cannot be reassigned once defined.

```
const SPEED_OF_LIGHT = 299792458
```

### Display Commands

*   `disp`: Show all defined variables and constants.
*   `disp vars`: Show only variables.
*   `disp consts`: Show only constants.

### Arbitrary Precision

Use the `to N places` syntax at the end of an expression to evaluate it numerically to a specific precision.

```
1/7 to 100 places
```

### Supported Functions

The tool supports a wide range of functions, including but not limited to:

*   **Trigonometric:** `sin`, `cos`, `tan`, `csc`, `sec`, `cot`
*   **Inverse Trig:** `asin`, `acos`, `atan`, etc.
*   **Roots:** `sqrt(x)`, `cbrt(x)`, `root(x, n)`
*   **Logarithms:** `log(x, base)`, `ln(x)`
*   **Calculus:** `diff(expr, var)`, `integrate(expr, var)`
*   **Solving:** `solve(equation, var)`
