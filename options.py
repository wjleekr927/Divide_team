# Option can be made here
# Take args
import argparse

def args_parser_main():
    parser = argparse.ArgumentParser()

    # Possible arguments
    # Option can be added here
    parser.add_argument('--special_num', type=int, default=0 , help="People who should be divided first")

    args = parser.parse_args()
    return args