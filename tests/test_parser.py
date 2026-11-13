# SPDX-FileCopyrightText: 2026 eightcraters <eightcraters@hotmail.com>
# SPDX-License-Identifier: Apache-2.0

from typing import Any

import pytest

from lua_api_parser import parser

SORT_ORDER_E0 = [
    {"order": 1},
    {"order": 2},
    {"order": 3},
]


# fmt: off
@pytest.mark.parametrize(
    "data, expected",
    [
        pytest.param(
            SORT_ORDER_E0,
            SORT_ORDER_E0,
            id="control",
        ),
        pytest.param(
            [
                {"order": 1},
                {"order": 3},
                {"order": 2},
            ],
            SORT_ORDER_E0,
            id="case_132",
        ),
        pytest.param(
            [
                {"order": 3},
                {"order": 1},
                {"order": 2},
            ],
            SORT_ORDER_E0,
            id="case_312",
        ),
        pytest.param(
            [
                {"order": 3},
                {"order": 2},
                {"order": 1},
            ],
            SORT_ORDER_E0,
            id="case_321",
        ),
    ],
)
def test_sort_order(data: list[Any], expected: list[Any]) -> None:
    # fmt: on
    parser.sort_order(data)
    assert data == expected
