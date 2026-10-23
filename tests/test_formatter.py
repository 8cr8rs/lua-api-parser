# SPDX-FileCopyrightText: 2026 eightcraters <eightcraters@hotmail.com>
# SPDX-License-Identifier: Apache-2.0

from typing import Any

import pytest

from fapi_parser import formatter

"""Notes: The assertation section for some normalizing functions will usually
begin with a 'control' section, where the desired result itself will be tested,
to ensure nothing is changed

Abbreviations unique to this file:
    e: expected - Expected result object from inputs
"""

# Weirdly enough, the fmt toggle tags cannot be placed after decorators

EMPTY_LINES_E0 = "a\nb\n"
# fmt: off
@pytest.mark.parametrize(
    "s, expected", [
        pytest.param(
            EMPTY_LINES_E0,
            EMPTY_LINES_E0,
            id="control",
        ),
        pytest.param(
            "a\n\nb\n\n",
            EMPTY_LINES_E0,
            id="duplicate_newlines",
        ),
        pytest.param(
            "\na\nb\n",
            EMPTY_LINES_E0,
            id="leading_newlines",
        )
    ]
)
def test_filter_empty_lines(s: str, expected: str) -> None:
    # fmt: on
    assert formatter.filter_empty_lines(s) == expected


# The params are out of order for easier readability
# prefix s should equal expected
# fmt: off
@pytest.mark.parametrize(
    "prefix, s, expected",
    [
        pytest.param(
            "--- ",
            "foo\nbar\nbaz\n",
            "--- foo\n--- bar\n--- baz\n",
            id="triple_line",
        ),
    ],
)
def test_prefix_lines(prefix: str, s: str, expected: str) -> None:
    # fmt: on
    assert formatter.prefix_lines(s, prefix) == expected


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
    formatter.sort_order(data)
    assert data == expected
