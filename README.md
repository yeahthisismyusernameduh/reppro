# Symbolic Math CLI Tool

A powerful, feature-rich command-line tool for symbolic mathematics, built in Python using the SymPy library. It can be used as an interactive calculator (REPL) or to evaluate scripts from a file.

## Features

*   **User-Defined Functions:** Create your own custom functions.
*   **Interactive REPL & File Evaluation:** Use it on the fly or run pre-written scripts.
*   **Stateful Memory:** Define and delete variables, constants, and functions that persist within a session.
*   **Symbolic Mathematics:** It's not just a calculator; it understands symbolic expressions.
*   **Calculus & Algebra:** Perform differentiation, integration, and solve equations.
*   **Flexible Syntax:** Supports multi-statement lines, quiet mode, and formatted numbers.
*   **Rich Function Library:** Includes a wide range of built-in mathematical functions.

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
> f(x) = x**2
Defined function f(x)
> f(5)
25
> diff f(x) wrt x
2*x
```

### 2. File Evaluator

For running a script of commands, use the `math_file_eval.py` script, passing the path to your file:

```bash
python3 math_file_eval.py path/to/your/script.txt
```

The script file should contain one command per line. Lines starting with `#` are treated as comments and are ignored.

## Commands & Syntax Reference

### General Syntax

*   **Multi-Statement Lines:** You can enter multiple commands on one line, separated by commas.
    ```
    x = 10, const C = 5, f(t) = C*t**2
    ```
*   **Quiet Mode:** To suppress the confirmation output for definitions and deletions, end the line with `--q`.
    ```
    my_var = 12345 --q
    ```
*   **Number Formatting:** You can use commas in numbers for readability. They will be ignored.
    ```
    1,000,000 / 2
    ```

### State Management

#### Variable and Constant Assignment
Use the `=` operator for variables and `const` for constants.
```
> my_var = 10 * 5
Defined variable 'my_var' = 50
> const PI_ISH = 3.14
Defined constant 'PI_ISH' = 3.14
```

#### User-Defined Functions
Define your own functions with a syntax similar to mathematical notation.
Function parameters are local to the function and will not be replaced by session variables with the same name.

**Syntax:** `<name>(<arg1>, <arg2>, ...) = <expression>`

**Examples:**
```
> f(x) = x**2
Defined function f(x)
> f(4)
16
> g(x,y) = x**2 + y
> g(2, 5)
9
> a = 10 --q
> g(a, 1)  # 'a' from the session is used as an argument
101
```

#### Deletion (`del`)
Use the `del` keyword to delete one or more variables, constants, or functions. You cannot delete built-in items.
```
del my_var, PI_ISH, f, g
```

#### Displaying State (`disp`)
*   `disp`: Shows all defined items, categorized into `Built-Ins`, `Constants`, and `Variables`.
*   `disp vars`: Shows only user-defined variables.
*   `disp consts`: Shows only user-defined constants.
*   `disp funcs`: Shows only user-defined functions.

**Example `disp funcs` output:**
```
Functions:
  f(x) = x**2
  g(x, y) = x**2 + y
```

---

### Expressions and Operations

#### Precision
*   **Default Precision:** Numerical results are formatted to a default precision (5 decimal places, where applicable).
*   **Arbitrary Precision:** Use the `to N places` syntax to evaluate an expression to a specific precision.
    ```
    > pi to 20 places
    3.14159265358979323846
    ```

#### Evaluation with Temporary Values (`eval`)
Evaluates an expression using temporary values for variables, without affecting the main session state.

**Syntax:** `eval <expression> for <var1>=<val1>, <var2>=<val2>, ...`

**Example:**
```
> x = 2 --q
> eval x + 1 for x = 10
11
> x
2
```

#### Expression Manipulation (`simp`, `exp`, `fac`)
*   `simp <expression>`: Attempts to simplify an expression.
*   `exp <expression>`: Expands an expression.
*   `fac <expression>`: Factorizes an expression.

**Example:**
```
> simp sin(x)**2 + cos(x)**2
1
> exp (x+y)**2
x**2 + 2*x*y + y**2
```

#### Calculus and Solving

*   **`diff <expr> [wrt <var>]`**: Calculates the derivative. The variable is optional if unambiguous.
*   **`solve <equation> [wrt <var>]`**: Solves an equation. The variable is optional if unambiguous.
*   **`int <expr> [wrt <var>] [from <a> to <b>]`**: Calculates the definite or indefinite integral. The `wrt` and `from...to` clauses are optional and can be in any order.

**Example:**
```
> diff x**3 + a*x wrt x
3*x**2 + a

> solve x**2 = 4
Solutions: x = -2, 2

> int x**2 from 0 to 1
1/2
```

---

### Built-In Functions and Constants
The tool supports a wide range of built-in functions (`sin`, `cos`, `log`, `sqrt`, etc.) and constants (`pi`, `e`, `tau`). These cannot be redefined or deleted.
