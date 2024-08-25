import argparse


def parse_args():
    parser = argparse.ArgumentParser(description='Compares two configuration \
                                           files and shows a difference.')

    parser.add_argument("filename1")
    parser.add_argument("filename2")
    parser.add_argument("-f", "--format", help="set format of output",
                        default='stylish', type=str)
    args = parser.parse_args()
    return args
