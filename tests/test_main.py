# SPDX-FileCopyrightText: 2026 eightcraters <eightcraters@hotmail.com>
# SPDX-License-Identifier: Apache-2.0

import fapi_parser


def test_main() -> None:
    # Just running main with zero input files should yield an exit code of 1.
    # Pass an empty list to prevent argparse from reading pytest's arguments.
    exit_code = fapi_parser.main([])
    assert exit_code == 1
