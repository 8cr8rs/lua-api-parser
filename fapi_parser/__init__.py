# SPDX-FileCopyrightText: 2026 eightcraters <eightcraters@hotmail.com>
# SPDX-License-Identifier: Apache-2.0

import logging
import json
from typing import Any

from . import output

# Do this before importing other modules
# They depend on the root logger. It only makes sense to do so.
output.setup_root_logger()

from . import (
    option,
)
from .parser import parse_json

def main(argv: list[str] | None = None) -> int:
    parser = option.build_parser()
    # The only reason the static type checker assumes the below value parse as
    # CustomArgs is due to the code generating the Namespace being at runtime.
    args: option.CustomArgs = parser.parse_args(argv) # pyright: ignore [reportAssignmentType]
    root_logger = logging.getLogger()
    root_logger.setLevel(args.log_level)

    logger = logging.getLogger(__name__)

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

    # if not args.input_files:
    #     logger.error("try --help!")
    # else:
    #     for file in args.input_files:
    #         data = parse_json_file(file)
    #         if not data:
    #             continue

    obj = parse_json_file("runtime-api.json")
    if not obj is None:
        parse_json(obj)
    return 0
