import sympy

class MathEvaluator:
    """
    A core class to handle the parsing and evaluation of mathematical expressions.
    It maintains the state of variables and constants.
    """
    def __init__(self):
        """
        Initializes the evaluator, setting up built-in constants.
        """
        # _state stores variables and constants.
        # The value is a tuple: (sympy_expression, is_constant)
        self._state = {
            'pi': (sympy.pi, True),
            'e': (sympy.E, True),
            'tau': (2 * sympy.pi, True), # Define tau as 2*pi
        }

    def evaluate(self, input_str: str):
        """
        Evaluates a single line of input.

        Args:
            input_str: The string to evaluate.

        Returns:
            The result of the evaluation, or a status message.
        """
        input_str = input_str.strip()
        if not input_str:
            return None

        # --- Handle Display Commands ---
        if input_str in ('disp', 'disp vars', 'disp consts'):
            output = []
            if input_str == 'disp':
                output.append("Constants:")
                output.extend(self._format_state(constants=True))
                output.append("\nVariables:")
                output.extend(self._format_state(constants=False))
            elif input_str == 'disp consts':
                output.append("Constants:")
                output.extend(self._format_state(constants=True))
            elif input_str == 'disp vars':
                output.append("Variables:")
                output.extend(self._format_state(constants=False))
            return "\n".join(output)

        # --- Handle Assignment ---
        is_const_assignment = input_str.startswith('const ')
        if '=' in input_str:
            if is_const_assignment:
                # Remove 'const ' part for parsing
                assign_str = input_str[6:]
            else:
                assign_str = input_str

            parts = assign_str.split('=', 1)
            var_name = parts[0].strip()
            expr_str = parts[1].strip()

            if not var_name.isidentifier():
                return "Error: Invalid name."

            if var_name in self._state and self._state[var_name][1]:
                return f"Error: Cannot reassign constant '{var_name}'."

            try:
                eval_context = {k: v[0] for k, v in self._state.items()}
                result_expr = sympy.sympify(expr_str, locals=eval_context)
                self._state[var_name] = (result_expr, is_const_assignment)
                return f"Defined {'constant' if is_const_assignment else 'variable'} {var_name}"
            except Exception as e:
                return f"Error: {e}"

        # --- Handle Expression Evaluation ---
        import re
        try:
            # Check for precision syntax first
            precision_match = re.search(r' to (\d+) places$', input_str)
            if precision_match:
                num_places = int(precision_match.group(1))
                # Get the core expression to evaluate
                core_expr_str = input_str[:precision_match.start()].strip()
            else:
                num_places = None
                core_expr_str = input_str

            # Set up the evaluation context with state and advanced functions
            eval_context = {k: v[0] for k, v in self._state.items()}

            # Add calculus, solving, and root functions to the context
            # Also add cbrt as a convenience function
            advanced_funcs = {
                'diff': sympy.diff,
                'integrate': sympy.integrate,
                'solve': sympy.solve,
                'root': sympy.root,
                'cbrt': lambda x: sympy.root(x, 3),
                'sin': sympy.sin, 'cos': sympy.cos, 'tan': sympy.tan,
                'csc': sympy.csc, 'sec': sympy.sec, 'cot': sympy.cot,
                'asin': sympy.asin, 'acos': sympy.acos, 'atan': sympy.atan,
                'acsc': sympy.acsc, 'asec': sympy.asec, 'acot': sympy.acot,
                'sqrt': sympy.sqrt,
                'log': sympy.log,
                'ln': lambda x: sympy.log(x),
            }
            eval_context.update(advanced_funcs)

            result = sympy.sympify(core_expr_str, locals=eval_context)

            # If a precision was specified, evaluate the result
            if num_places is not None:
                # Use .evalf() for numerical evaluation to N decimal places
                result = result.evalf(num_places)

            return result
        except Exception as e:
            return f"Error: {e}"

    def _format_state(self, constants: bool) -> list[str]:
        """Helper to format variables or constants for display."""
        items = []
        for name, (value, is_const) in sorted(self._state.items()):
            if is_const == constants:
                items.append(f"  {name} = {value}")
        if not items:
            items.append("  (none)")
        return items


if __name__ == '__main__':
    evaluator = MathEvaluator()
    print("--- Testing MathEvaluator ---")

    # Test 1-7: Previous tests
    print("... (previous tests) ...")
    evaluator.evaluate('x = 10')
    evaluator.evaluate('x = x + 1')

    # Test 8: Constant assignment
    print(f"\nInput: 'const my_c = 42' -> Output: {evaluator.evaluate('const my_c = 42')}")
    print(f"Input: 'my_c' -> Output: {evaluator.evaluate('my_c')}")

    # Test 9: Trying to reassign a new constant
    print(f"Input: 'my_c = 43' -> Output: {evaluator.evaluate('my_c = 43')}")

    # Test 10: Display variables
    print(f"\n--- disp vars ---")
    print(evaluator.evaluate('disp vars'))

    # Test 11: Display constants
    print(f"\n--- disp consts ---")
    print(evaluator.evaluate('disp consts'))

    # Test 12: Display all
    print(f"\n--- disp ---")
    print(evaluator.evaluate('disp'))
