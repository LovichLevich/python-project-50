#!/usr/bin/env python3
import gendiff


def main():
    args = gendiff.cli.parse_args()
    print(gendiff.generate_diff(args.filename1, args.filename2, args.format))


if __name__ == '__main__':
    main()