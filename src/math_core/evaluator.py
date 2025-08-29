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
        self.DEFAULT_PRECISION = 6 # Use 6 for pi to show 3.14159
        self._built_in_names = ['pi', 'e', 'tau']
        # _state stores variables and constants.
        # The value is a tuple: (sympy_expression, is_constant)
        self._state = {
            'pi': (sympy.pi, True),
            'e': (sympy.E, True),
            'tau': (2 * sympy.pi, True),
        }

    def evaluate(self, input_str: str):
        """
        Evaluates a single line of input, which may contain multiple statements.
        """
        import re

        # --- Pre-processing Step ---
        is_quiet = input_str.strip().endswith('--q')
        if is_quiet:
            input_str = input_str.strip()[:-3].strip()

        input_str = re.sub(r'(?<=\d),(?=\d)', '', input_str)

        # Handle 'del' command before splitting by comma
        if input_str.strip().startswith('del '):
            statements = [input_str.strip()]
        else:
            statements = re.split(r',(?![^\(]*\))', input_str)

        results = []
        for statement in statements:
            statement = statement.strip()
            if not statement:
                continue

            result = self._evaluate_statement(statement)
            if result is not None:
                results.append(str(result))

        if is_quiet or not results:
            return None

        return "\n".join(results)

    def _evaluate_statement(self, statement_str: str):
        """
        Evaluates a single, pre-processed statement.
        """
        import re

        # --- Handle diff and solve with new 'wrt' syntax ---
        m = re.match(r'^(diff|solve)\s+(.*?)(?:\s+wrt\s+(\w+))?$', statement_str, re.IGNORECASE)
        if m:
            command, expr_str, var_str = m.groups()
            command = command.lower()

            # Improve error handling for trailing 'wrt'
            if 'wrt' in statement_str.lower().rsplit(None, 2)[-2:] and not var_str:
                return f"Error: Missing variable after 'wrt'."

            try:
                # Auto-detect variable if not provided
                if not var_str:
                    temp_expr_str = expr_str
                    if '=' in temp_expr_str:
                        lhs_str, rhs_str = temp_expr_str.split('=', 1)
                        lhs_sym = self._sympify_expression(lhs_str)
                        rhs_sym = self._sympify_expression(rhs_str)
                        free_symbols = lhs_sym.free_symbols.union(rhs_sym.free_symbols)
                    else:
                        symbolic_expr = self._sympify_expression(temp_expr_str)
                        free_symbols = symbolic_expr.free_symbols

                    if len(free_symbols) == 1:
                        var_str = str(free_symbols.pop())
                    elif len(free_symbols) > 1:
                        return f"Error: Ambiguous expression. Please specify a variable using 'wrt'."

                # If we have a variable (specified or detected), proceed.
                if var_str:
                    eval_context = self._get_limited_context(var_str)
                    var_symbol = sympy.Symbol(var_str)

                    if command == 'diff':
                        expr = sympy.sympify(expr_str, locals=eval_context)
                        result = sympy.diff(expr, var_symbol)
                    else: # solve
                        if '=' in expr_str:
                            lhs_str, rhs_str = expr_str.split('=', 1)
                            lhs = sympy.sympify(lhs_str.strip(), locals=eval_context)
                            rhs = sympy.sympify(rhs_str.strip(), locals=eval_context)
                            equation = sympy.Eq(lhs, rhs)
                        else:
                            expr = sympy.sympify(expr_str, locals=eval_context)
                            equation = expr # Assume it's set to 0
                        result = sympy.solve(equation, var_symbol)

                    # Custom formatting for solve
                    if command == 'solve':
                        formatted_results = [self._format_output(r, None) for r in result]
                        return f"Solutions: {var_symbol.name} = {', '.join(formatted_results)}"
                    else:
                        return self._format_output(result, None)

                else: # No variable specified or found (e.g., 'diff 5')
                    if command == 'diff':
                        return 0
                    else:
                        return "Error: Cannot solve a constant expression."
            except Exception as e:
                return f"Error in {command}: {e}"

        # --- Handle simp, exp, fac ---
        m_manip = re.match(r'^(simp|exp|fac)\s+(.*)', statement_str, re.IGNORECASE)
        if m_manip:
            command, expr_str = m_manip.groups()
            command = command.lower()
            try:
                # Get the symbolic expression for the argument
                symbolic_expr = self._sympify_expression(expr_str)

                # If the expression is just a single symbol that is a variable in our state,
                # then we operate on the expression stored in that variable.
                if symbolic_expr.is_Symbol and str(symbolic_expr) in self._state:
                    # We operate on the expression stored in the variable
                    symbolic_expr = self._state[str(symbolic_expr)][0]

                # Perform the symbolic operation
                if command == 'simp':
                    result = sympy.simplify(symbolic_expr)
                elif command == 'exp':
                    result = sympy.expand(symbolic_expr)
                else: # fac
                    result = sympy.factor(symbolic_expr)

                # These commands return a symbolic result, not a fully evaluated number
                return self._format_output(result, None)
            except Exception as e:
                return f"Error in {command}: {e}"

        # --- Handle `int` command ---
        if statement_str.lower().startswith('int '):
            # Strip 'int ' from the front
            work_str = statement_str[4:].strip()

            var_str = None
            lower_bound_str = None
            upper_bound_str = None

            # Staged parsing
            # Look for 'wrt'
            wrt_match = re.search(r'\s+wrt\s+(\w+)', work_str, re.IGNORECASE)
            if wrt_match:
                var_str = wrt_match.group(1)
                # Remove the matched part from the string
                work_str = work_str[:wrt_match.start()] + work_str[wrt_match.end():]

            # Look for 'from ... to ...'
            from_match = re.search(r'\s+from\s+(.*?)\s+to\s+(.*)', work_str, re.IGNORECASE)
            if from_match:
                lower_bound_str = from_match.group(1).strip()
                upper_bound_str = from_match.group(2).strip()
                # Remove the matched part
                work_str = work_str[:from_match.start()] + work_str[from_match.end():]

            expr_str = work_str.strip()

            try:
                # Auto-detect variable if not provided
                if not var_str:
                    symbolic_expr = self._sympify_expression(expr_str)
                    free_symbols = symbolic_expr.free_symbols
                    if len(free_symbols) == 1:
                        var_str = str(free_symbols.pop())
                    elif len(free_symbols) > 1:
                        return f"Error: Ambiguous expression. Please specify a variable using 'wrt'."

                # If we have a variable, proceed.
                if var_str:
                    var_symbol = sympy.Symbol(var_str)
                    eval_context = self._get_limited_context(var_str)
                    expr = sympy.sympify(expr_str, locals=eval_context)

                    # Definite Integration
                    if lower_bound_str is not None and upper_bound_str is not None:
                        # Bounds can be expressions themselves, so sympify them with full context
                        full_context = self._get_limited_context(None)
                        lower = sympy.sympify(lower_bound_str, locals=full_context)
                        upper = sympy.sympify(upper_bound_str, locals=full_context)
                        result = sympy.integrate(expr, (var_symbol, lower, upper))
                    # Indefinite Integration
                    else:
                        result = sympy.integrate(expr, var_symbol)
                        C = sympy.Symbol('C')
                        result += C

                    return self._format_output(result, None)

                else: # No variable (e.g., int 5)
                    const_expr = self._sympify_expression(expr_str)
                    if const_expr.is_number:
                        return "Error: Please specify a variable to integrate a constant."
                    else: # Should not be reached if logic is correct
                        return "Error: Could not determine variable for integration."

            except Exception as e:
                return f"Error in int: {e}"


        # --- Handle Display Commands ---
        if statement_str in ('disp', 'disp vars', 'disp consts'):
            return self._format_state_new(statement_str)

        # --- Handle Deletion ---
        if statement_str.startswith('del '):
            names_str = statement_str[4:]
            names_to_delete = [name.strip() for name in names_str.split(',')]

            deleted, errors = [], []
            for name in names_to_delete:
                if not name: continue
                if name in self._built_in_names:
                    errors.append(f"Cannot delete built-in '{name}'")
                elif name in self._state:
                    del self._state[name]
                    deleted.append(name)
                else:
                    errors.append(f"Name '{name}' not found")

            response_parts = []
            if deleted:
                response_parts.append(f"Deleted: {', '.join(deleted)}")
            if errors:
                response_parts.append(f"Errors: {', '.join(errors)}")
            return ". ".join(response_parts) if response_parts else "No action taken."

        # --- Handle Assignment ---
        is_const_assignment = statement_str.startswith('const ')
        if '=' in statement_str:
            if is_const_assignment:
                assign_str = statement_str[6:]
            else:
                assign_str = statement_str

            parts = assign_str.split('=', 1)
            var_name = parts[0].strip()
            expr_str = parts[1].strip()

            if not var_name.isidentifier() or var_name in self._built_in_names:
                return f"Error: Invalid or protected name '{var_name}'."

            if var_name in self._state and self._state[var_name][1]:
                return f"Error: Cannot reassign constant '{var_name}'."

            try:
                symbolic_expr, _ = self._parse_expression(expr_str)

                # Check for undefined symbols before assignment
                for symbol in symbolic_expr.free_symbols:
                    if str(symbol) not in self._state:
                        return f"Error: Name '{symbol}' is not defined."

                self._state[var_name] = (symbolic_expr, is_const_assignment)

                evaluated_value = self._evaluate_for_display(symbolic_expr)
                formatted_value = self._format_output(evaluated_value, None)
                return f"Defined {'constant' if is_const_assignment else 'variable'} {var_name} = {formatted_value}"
            except Exception as e:
                return f"Error: {e}"

        # --- Handle Expression Evaluation ---
        try:
            symbolic_expr, num_places = self._parse_expression(statement_str)

            # Check for undefined symbols
            for symbol in symbolic_expr.free_symbols:
                if str(symbol) not in self._state:
                    return f"Error: Name '{symbol}' is not defined."

            final_value = self._evaluate_for_display(symbolic_expr)
            return self._format_output(final_value, num_places)
        except Exception as e:
            return f"Error: {e}"

    def _evaluate_for_display(self, expr):
        subs_dict = {k: v[0] for k, v in self._state.items()}
        return expr.subs(subs_dict)

    def _format_output(self, value, num_places) -> str:
        if isinstance(value, list):
            return str([self._format_output(item, num_places) for item in value])

        if hasattr(value, 'is_number') and value.is_number:
            prec = num_places if num_places is not None else self.DEFAULT_PRECISION
            # Use evalf for floating point results
            if not value.is_Integer:
                value = value.evalf(prec)

            s = str(value)
            if '.' in s:
                s = s.rstrip('0').rstrip('.')
            return s

        return str(value)

    def _parse_expression(self, expr_str: str):
        import re

        precision_match = re.search(r' to (\d+) places$', expr_str)
        if precision_match:
            num_places = int(precision_match.group(1))
            core_expr_str = expr_str[:precision_match.start()].strip()
        else:
            num_places = None
            core_expr_str = expr_str

        symbolic_expr = self._sympify_expression(core_expr_str)
        return symbolic_expr, num_places

    def _sympify_expression(self, expr_str: str):
        eval_context = {
            'diff': sympy.diff, 'integrate': sympy.integrate, 'solve': sympy.solve,
            'root': sympy.root, 'cbrt': lambda x: sympy.root(x, 3),
            'sin': sympy.sin, 'cos': sympy.cos, 'tan': sympy.tan,
            'csc': sympy.csc, 'sec': sympy.sec, 'cot': sympy.cot,
            'asin': sympy.asin, 'acos': sympy.acos, 'atan': sympy.atan,
            'acsc': sympy.acsc, 'asec': sympy.asec, 'acot': sympy.acot,
            'sqrt': sympy.sqrt, 'log': sympy.log, 'ln': lambda x: sympy.log(x),
        }

        for var_name in self._state.keys():
            eval_context[var_name] = sympy.Symbol(var_name)

        return sympy.sympify(expr_str, locals=eval_context)

    def _get_limited_context(self, var_to_exclude: str | None) -> dict:
        """Builds an evaluation context containing functions and state variables,
        optionally excluding one variable to treat it as a symbol."""

        eval_context = {
            'root': sympy.root, 'cbrt': lambda x: sympy.root(x, 3),
            'sin': sympy.sin, 'cos': sympy.cos, 'tan': sympy.tan,
            'csc': sympy.csc, 'sec': sympy.sec, 'cot': sympy.cot,
            'asin': sympy.asin, 'acos': sympy.acos, 'atan': sympy.atan,
            'acsc': sympy.acsc, 'asec': sympy.asec, 'acot': sympy.acot,
            'sqrt': sympy.sqrt, 'log': sympy.log, 'ln': lambda x: sympy.log(x),
        }
        for k, v in self._state.items():
            if k != var_to_exclude:
                eval_context[k] = v[0]
        return eval_context

    def _format_state_new(self, command: str) -> str:
        """Formats the current state for display based on the command."""
        built_ins, user_consts, user_vars = [], [], []

        for name, (value, is_const) in sorted(self._state.items()):
            # Evaluate the value for display
            display_val = self._evaluate_for_display(value)
            # Format it
            formatted_val = self._format_output(display_val, None)

            line = f"  {name} = {formatted_val}"
            if name in self._built_in_names:
                built_ins.append(line)
            elif is_const:
                user_consts.append(line)
            else:
                user_vars.append(line)

        output = []
        if command == 'disp':
            output.append("Built-Ins:")
            output.extend(built_ins if built_ins else ["  (none)"])
            output.append("") # Add blank line
            output.append("Constants:")
            output.extend(user_consts if user_consts else ["  (none)"])
            output.append("") # Add blank line
            output.append("Variables:")
            output.extend(user_vars if user_vars else ["  (none)"])
        elif command == 'disp consts':
            output.append("Constants:")
            output.extend(user_consts if user_consts else ["  (none)"])
        elif command == 'disp vars':
            output.append("Variables:")
            output.extend(user_vars if user_vars else ["  (none)"])

        return "\n".join(output)


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
