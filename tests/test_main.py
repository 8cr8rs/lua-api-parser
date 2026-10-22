# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2026 eightcraters <eightcraters@hotmail.com>
# SPDX-License-Identifier: Apache-2.0

import pytest

import fapi_parser


# just running main with no arguments
# it should NOT error without anything passed
def test_main():
    try:
        # pass an empty list to prevent argparse from reading pytest's arguments
        exit_code = fapi_parser.main([])
        assert exit_code == 0
    except Exception as e:
        pytest.fail(f"Unexpected error occurred running main:\n{e}")
