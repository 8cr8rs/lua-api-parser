# SPDX-FileCopyrightText: 2026 eightcraters <eightcraters@hotmail.com>
# SPDX-License-Identifier: Apache-2.0

import pytest

from fapi_parser import option


def test_build_parser() -> None:
    try:
        _ = option.build_parser()
    except Exception as e:
        pytest.fail(f"Parser builder raised an unexpected error:\n{e}")
