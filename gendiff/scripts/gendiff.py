#!/usr/bin/env python
from gendiff.engine import generate_diff
from gendiff.helpers.cli import parse_arguments


def main():
    args = parse_arguments()
    print(generate_diff(args.first_file, args.second_file, args.format))


if __name__ == "__main__":
    main()
