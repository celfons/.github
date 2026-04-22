#!/usr/bin/env python3
"""context-mesh/scripts/trim-context.py

Trims text input to a maximum token count, preserving the most recent (tail)
content. Tokens are approximated as 4 characters each.

Usage:
    echo "text" | python3 trim-context.py [--max-tokens N]
    python3 trim-context.py [file] [--max-tokens N]
"""

import argparse
import sys

CHARS_PER_TOKEN = 4
# Maximum characters to scan from the cut point when looking for a clean line
# boundary. Keeps alignment fast while handling most real-world line lengths.
MAX_NEWLINE_SEARCH = 200


def trim_to_tokens(text: str, max_tokens: int) -> str:
    max_chars = max_tokens * CHARS_PER_TOKEN
    if len(text) <= max_chars:
        return text
    truncated = text[-max_chars:]
    # Align to the nearest line boundary to avoid mid-line truncation
    newline_pos = truncated.find("\n")
    if 0 < newline_pos < MAX_NEWLINE_SEARCH:
        truncated = truncated[newline_pos + 1 :]
    return f"[...trimmed: showing last ~{max_tokens} tokens...]\n\n{truncated}"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Trim text to a maximum token count, keeping the most recent content."
    )
    parser.add_argument(
        "input",
        nargs="?",
        default="-",
        help="Input file path (default: stdin)",
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=4000,
        help="Maximum number of tokens (default: 4000)",
    )
    args = parser.parse_args()

    if args.input == "-":
        text = sys.stdin.read()
    else:
        with open(args.input, encoding="utf-8") as fh:
            text = fh.read()

    sys.stdout.write(trim_to_tokens(text, args.max_tokens))


if __name__ == "__main__":
    main()
