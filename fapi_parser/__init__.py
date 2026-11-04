# SPDX-FileCopyrightText: 2026 eightcraters <eightcraters@hotmail.com>
# SPDX-License-Identifier: Apache-2.0

import logging
import json
from typing import Any

from . import output

# Setting up logger before importing other modules
# They depend on the root logger. It only makes sense to do so.
output.setup_root_logger()

from . import (
    option,
    parser,
)

def main(argv: list[str] | None = None) -> int:
    argument_parser = option.build_parser()
    # The only reason the static type checker assumes the below value parse as
    # CustomArgs is due to the code generating the Namespace being at runtime.
    args: option.CustomArgs = argument_parser.parse_args(argv) # pyright: ignore [reportAssignmentType]

    root_logger = logging.getLogger()
    root_logger.setLevel(args.log_level)

    logger = logging.getLogger(__name__)
    logger.debug("Logger initialized")

    logger.debug(args)

    def parse_json_file(file_path: str) -> dict[str, Any] | None:
        """Parses a JSON object from a file"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"{file_path} does not exist")
        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode JSON file {file_path}", e)
        return None

    if len(args.input_files) < 1:
        logger.error("No input files given.")
        return 1

    for input_file in args.input_files:
        obj = parse_json_file(input_file)
        if not obj is None:
            logger.info("Program is working")
            parser.parse_json(obj)

    return 0
