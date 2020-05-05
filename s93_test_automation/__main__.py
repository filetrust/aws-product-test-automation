

from s93_test_automation import run_tests
import argparse
import logging
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger("glasswall")
import os
import unittest


def get_command_line_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--product", "-p",
        dest="product",
        help="Name of product to test.",
        type=str,
        required=True
    )
    parser.add_argument(
        "--endpoint", "-e",
        dest="endpoint",
        help="API Gateway endpoint URL.",
        type=str,
        required=True
    )
    parser.add_argument(
        "--api_key", "-a",
        dest="api_key",
        help="API key to access endpoint.",
        type=str,
        required=True
    )
    parser.add_argument(
        "--test_files", "-t",
        dest="test_files",
        help="Path to directory containing external test files.",
        type=str,
        default=os.path.join("data", "files", "external")
    )

    return parser.parse_args()


def set_environment_variables(args):
    os.environ["endpoint"]      = args.endpoint
    os.environ["api_key"]       = args.api_key
    os.environ["test_files"]    = args.test_files


def main():
    args = get_command_line_args()
    set_environment_variables(args)

    run_tests.run(product=args.product)


if __name__ == "__main__":
    main()
