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

@pytest.mark.parametrize(
    "s, expected",
    [
        (
            (
                "a\n"
                "b\n"
            ),
            (
                "a\n"
                "b\n"
            )
        ),
        (
            (
                "a\n"
                "\n"
                "b\n"
            ),
            (
                "a\n"
                "b\n"
            )
        )
    ]
)
def test_filter_empty_lines(s: str, expected: str) -> None:
    assert formatter.filter_empty_lines(s) == expected


# The params are out of order for easier readability
@pytest.mark.parametrize(
    "prefix, s, expected",
    [
        (
            "--- ",
            (
                "foo\n"
                "bar\n"
                "baz\n"
            ),
            (
                "--- foo\n"
                "--- bar\n"
                "--- baz\n"
            )
        )
    ]
)
def test_prefix_lines(prefix: str, s: str, expected: str) -> None:
    assert formatter.prefix_lines(s, prefix) == expected


SORT_ORDER_E1 = [
    { "order": 1 },
    { "order": 2 },
    { "order": 3 },
]
@pytest.mark.parametrize(
    "data, expected",
    [
        pytest.param(
            [
                { "order": 3 },
                { "order": 1 },
                { "order": 2 },
            ],
            SORT_ORDER_E1,
        ),
        pytest.param(
            [
                { "order": 1 },
                { "order": 3 },
                { "order": 2 },
            ],
            SORT_ORDER_E1,
        ),
        pytest.param(
            [
                { "order": 3 },
                { "order": 2 },
                { "order": 1 },
            ],
            SORT_ORDER_E1,
        ),
    ]
)
def test_sort_order(data: dict[str, Any], expected: dict[str, Any]) -> None:
    formatter.sort_order(data)
    assert data == expected
