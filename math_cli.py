from src.math_core.evaluator import MathEvaluator
import sys

def get_version():
    """Reads the version from the VERSION file."""
    try:
        with open('VERSION', 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return "0.0.0"

def main():
    """
    Main function to run the interactive REPL.
    """
    version = get_version()
    print(f"Welcome to the Math CLI! (Version {version})")
    print("Enter expressions to evaluate, or 'quit' to exit.")
    evaluator = MathEvaluator()

    while True:
        try:
            # Get input from the user
            input_str = input("> ")

            # Check for exit command
            if input_str.lower() in ('quit', 'exit'):
                break

            # Evaluate the input
            result = evaluator.evaluate(input_str)

            # Print the result
            if result is not None:
                print(result)

        except (KeyboardInterrupt, EOFError):
            # Handle Ctrl+C or Ctrl+D
            print("\nExiting.")
            break
        except Exception as e:
            # Catch any other unexpected errors
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
