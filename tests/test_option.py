# SPDX-FileCopyrightText: 2026 eightcraters <eightcraters@hotmail.com>
# SPDX-License-Identifier: Apache-2.0

from argparse import ArgumentError

import pytest

from lua_api_parser import option


def test_build_parser() -> None:
    try:
        _ = option.build_parser()
    except (ArgumentError, TypeError, ValueError) as e:
        pytest.fail(f"Parser builder raised an unexpected error:\n{e}")
