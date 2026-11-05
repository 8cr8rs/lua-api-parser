# SPDX-FileCopyrightText: 2026 eightcraters <eightcraters@hotmail.com>
# SPDX-License-Identifier: Apache-2.0

import pytest

from fapi_parser import formatter

# Weirdly enough, fmt toggle tags for Ruff cannot be placed after decorators, so
# their closing comment will be placed at the first line of functions which do
# have them.

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
