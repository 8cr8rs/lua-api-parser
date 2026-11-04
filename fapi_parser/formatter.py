# SPDX-FileCopyrightText: 2026 eightcraters <eightcraters@hotmail.com>
# SPDX-License-Identifier: Apache-2.0

from typing import Any


def filter_empty_lines(s: str) -> str:
    """Removes empty lines of a string and returns it"""
    return "\n".join([line for line in s.splitlines() if line.strip()]) + "\n"


def prefix_lines(s: str, prefix: str) -> str:
    """Prefixes each line of a string with prefix and returns it"""
    return (
        "\n".join(
            # preserve spacing with rstrip but do not remove empty lines
            [(prefix + line).rstrip() for line in s.splitlines()]
        )
        + "\n"
    )


def comment_lines(s: str) -> str:
    return prefix_lines(s, prefix="--- ")
