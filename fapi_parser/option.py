# SPDX-FileCopyrightText: 2026 eightcraters <eightcraters@hotmail.com>
# SPDX-License-Identifier: Apache-2.0

import argparse
import logging

from collections.abc import Iterable
from typing import Protocol, override


def str_to_bool(value: str) -> bool:
    if value.lower() in ("true", "yes", "t", "y", "1"):
        return True
    elif value.lower() in ("false", "no", "f", "n", "0"):
        return False
    else:
        raise argparse.ArgumentTypeError(
            f"Boolean string expected, got {type(value)} from {value}."
        )


class HelpFormatter(argparse.HelpFormatter):
    @override
    def _format_usage(
        self,
        usage: str | None,
        actions: Iterable[argparse.Action],
        groups: Iterable[argparse._MutuallyExclusiveGroup],
        prefix: str | None,
    ) -> str:
        return super()._format_usage(usage, actions, groups, prefix)

    @override
    def _format_action(self, action: argparse.Action) -> str:
        return super()._format_action(action)


class CustomArgs(Protocol):
    """Interface class for argument typing suggestions"""

    input_files: list[str]
    log_level: int
    onefile: bool
    output_dir: str
    output_ext: str


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="factorio-api-docs-generator",
        usage="%(prog)s [options]",
        description=(
            "A CLI to convert JSONdocs from Factorio's online API into "
            "lua_ls/EmmyLua LSP parsable type definitions."
        ),
        add_help=False,
        conflict_handler="resolve",
        formatter_class=HelpFormatter,
    )

    # ===============
    # General Options
    # ===============

    general = parser.add_argument_group("General Options")
    general.add_argument(
        "-h",
        "--help",
        action="help",
        help="Print this help message and exit",
    )
    general.add_argument(
        "--version",
        action="version",
        version="%(prog)s",
        help="Print program version and exit",
    )

    # ==============
    # Output Options
    # ==============

    output = parser.add_argument_group("Output Options")
    output_console = output.add_mutually_exclusive_group()
    output_console.add_argument(
        "-v",
        "--verbose",
        action="store_const",
        dest="log_level",
        default=logging.INFO,
        const=logging.DEBUG,
        help="Debug logging mode",
    )

    # ============
    # File Options
    # ============

    file = parser.add_argument_group("File Options")
    file.add_argument(
        "-P",
        dest="output_dir",
        help="Output directory for files",
    )
    file.add_argument(
        "--ext",
        "--extension",
        action="store",
        dest="output_ext",
        default="d.lua",
        help="Output file extension",
    )
    file.add_argument(
        "--onefile",
        dest="onefile",
        nargs="?",
        const=True,
        default=False,
        type=str_to_bool,
        help="Output type definitions as one file",
    )

    # Positional arguments
    parser.add_argument(
        "input_files",
        nargs=argparse.REMAINDER,
    )
    return parser
