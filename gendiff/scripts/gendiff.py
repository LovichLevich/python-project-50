#!/usr/bin/env python
from gendiff.engine import generate_diff
from gendiff.helpers.cli import parse_arguments


def main():
    args = parse_arguments()
    if args.format == 'plain':
        formatter = 'plain'
    elif args.format == 'json':
        formatter = 'json'
    elif args.format == 'stylish':
        formatter = 'stylish'
    else:
        raise ValueError(f"Unknown format: {args.format}")
    print(generate_diff(args.first_file, args.second_file, formatter))


if __name__ == "__main__":
    main()
