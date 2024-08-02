#!/usr/bin/env python
import argparse
from gendiff.engine import generate_diff
from gendiff.filters.plain import plain
from gendiff.filters.stylish import stylish


def main():
    parser = argparse.ArgumentParser(
        description='Compares two configuration files and shows a difference.')
    parser.add_argument(
        "-f",
        "--format",
        dest="format",
        default="stylish",
        help="Set format of output (default: stylish)")
    parser.add_argument('first_file')
    parser.add_argument('second_file')
    args = parser.parse_args()
    if args.format == 'plain':
        formatter = plain
    elif args.format == 'stylish':
        formatter = stylish
    print(generate_diff(args.first_file, args.second_file, formatter))


if __name__ == "__main__":
    main()
