from src.math_core.evaluator import MathEvaluator
import sys

def main():
    """
    Main function to run the interactive REPL.
    """
    print("Welcome to the Math CLI!")
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
