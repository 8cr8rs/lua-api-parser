#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2026 eightcraters <eightcraters@hotmail.com>
# SPDX-License-Identifier: Apache-2.0

import argparse
from pathlib import Path

import pytest

TEST_DIR = str(Path("./tests").resolve())


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        add_help=False,
    )
    general = parser.add_argument_group("General Options")
    general.add_argument(
        "-h",
        "--help",
        action="help",
        help="Print this help message and exit",
    )
    test = parser.add_argument_group("Test Options")
    test.add_argument(
        "--cov",
        "--coverage",
        action="store_true",
        dest="coverage",
        help="Generate coverage report",
    )
    test.add_argument(
        "--cov-report",
        action="store",
        default="html",
        dest="coverage_report",
        help="Coverage report type",
    )
    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    pytest_args = [TEST_DIR, "-v", "--cov", "--cov-report", "html"]
    # keep the args away for now
    # if args.coverage:
    #     pytest_args.append("--cov")
    # if args.coverage_report:
    #     pytest_args.append(f"--cov-report={args.coverage_report}")

    exit_code = pytest.main(pytest_args)
    print(f"Pytest exited with code: {exit_code}")


if __name__ == "__main__":
    main()
