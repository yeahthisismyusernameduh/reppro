import argparse

def add(args):
    """Adds two numbers."""
    result = args.n1 + args.n2
    print(result)

def main():
    """Main function for the math CLI tool."""
    parser = argparse.ArgumentParser(description="A simple math CLI tool.")
    subparsers = parser.add_subparsers(dest="command", help="sub-command help")
    subparsers.required = True

    # Create the parser for the "add" command
    parser_add = subparsers.add_parser("add", help="adds two numbers")
    parser_add.add_argument("n1", type=float, help="The first number")
    parser_add.add_argument("n2", type=float, help="The second number")
    parser_add.set_defaults(func=add)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
