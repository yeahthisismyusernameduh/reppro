from src.math_core.evaluator import MathEvaluator
import argparse
import sys

def main():
    """
    Main function to run the file-based evaluator.
    """
    parser = argparse.ArgumentParser(description="Evaluate a file with math expressions.")
    parser.add_argument("filepath", help="The path to the file to evaluate.")
    args = parser.parse_args()

    try:
        with open(args.filepath, 'r') as f:
            evaluator = MathEvaluator()
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'): # Ignore empty lines and comments
                    result = evaluator.evaluate(line)
                    if result is not None:
                        # For disp, the result is already formatted multiline
                        if "Constants:" in str(result) or "Variables:" in str(result):
                            print(f"In:  {line}\nOut:\n{result}\n")
                        else:
                            print(f"In:  {line}\nOut: {result}\n")

    except FileNotFoundError:
        print(f"Error: File not found at '{args.filepath}'", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
