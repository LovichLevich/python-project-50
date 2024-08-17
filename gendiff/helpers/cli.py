import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Compares two configuration files and shows a difference.'
    )
    parser.add_argument(
        "-f",
        "--format",
        dest="format",
        default="stylish",
        help="Set format of output (default: stylish)"
    )
    parser.add_argument('first_file')
    parser.add_argument('second_file')
    return parser.parse_args()
