#!/bin/python3

import sys
from collections import defaultdict
from decimal import Decimal, InvalidOperation


def parse_line(line: list[str]) -> tuple[Decimal, str] | None:
    if (
        len(line) == 2
    ):  # COMMENT - Check to ensure the line is correctly formatted with exactly two parts (amount and currency). If not, we skip it.
        # COMMENT - Python Tuple unpacking
        amount_str, currency = line
        try:
            # COMMENT - Ensure amount is a Decimal before adding
            amount: Decimal = Decimal(amount_str)
            return (amount, currency)
        # COMMENT - If Decimal fails, error malformed line and continue, rather than crash
        except InvalidOperation:
            # COMMENT - Log or handle unexpected data
            print(f"Skipping malformed amount: '{amount_str}'", file=sys.stderr)
            return None
    else:
        print(
            f"Skipping malformed line length: expected 2 parts, got '{len(line)}'",
            file=sys.stderr,
        )
        return None


def aggregate_totals(data: defaultdict[str, Decimal]) -> None:
    for currency, total in sorted(data.items()):
        # COMMENT - f-strings and two decimal places for currency format
        print(f"{currency}: {total:.2f}")


def read_lines(filepath: str) -> None:
    # 1. Choose the right data structure (defaultdict(Decimal) is perfect for sums)
    totals: defaultdict[str, Decimal] = defaultdict(Decimal)

    # 2. Robust File Handling
    try:
        # COMMENT - with statement ensures file handle f is automatically closed, even in event of error - prevents memory leaks
        # COMMENT - 'r' Opens file in readonly mode
        with open(filepath, "r") as f:
            # COMMENT - iterates line by line through the line, memory efficient
            # COMMENT - ...if we opened entire file this would not scale to large files potentially
            for line in f:
                # 3. Clean Parsing & Error Prevention
                # COMMENT - strip() removes leading/trailing whitespace including /n
                # COMMENT - split() splits by whitespace (default) creating list of strings (e.g. ['100.50', 'USD']).
                parts = line.strip().split()
                result = parse_line(parts)
                if result:
                    amount, currency = result
                    totals[
                        currency
                    ] += amount  # COMMENT - defaultdict starts at 0.00 for a new key, otherwise adds amount

    # COMMENT - Global error handlers, using stderr so as not to pollute the output
    except IndexError:  # COMMENT - catching out of range issues
        print("Usage: python3 script.py <filename>", file=sys.stderr)
        # COMMENT - non zero exit identifies failure
        sys.exit(1)
    except FileNotFoundError:
        print(f"Error: File not found at '{filepath}'", file=sys.stderr)
        sys.exit(1)

    # 4. Final Output Formatting
    aggregate_totals(totals)


# COMMENT - Only run the code inside this block directly (not imported)
if __name__ == "__main__":
    if len(sys.argv) < 2:
        # Handling the missing argument from the command line
        print(
            "Error: Missing file argument. Usage: python3 script.py <filename>",
            file=sys.stderr,
        )
        sys.exit(1)
    else:
        # Pass the first argument (the filename) to main
        read_lines(sys.argv[1])
