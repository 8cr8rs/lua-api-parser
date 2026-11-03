# SPDX-FileCopyrightText: 2026 eightcraters <eightcraters@hotmail.com>
# SPDX-License-Identifier: Apache-2.0

import sys
import logging

from datetime import datetime, timezone
from typing import override

LOG_FORMAT = "[%(name)s] [%(levelname)s] [%(asctime)s] %(message)s"


class Formatter(logging.Formatter):
    @override
    def format(
        self,
        record: logging.LogRecord
    ) -> str:
        # formats log level name as lowercase
        record.levelname = record.levelname.lower()
        return super().format(record)

    @override
    def formatTime(
        self,
        record: logging.LogRecord,
        datefmt: str | None = None
    ) -> str:
        # formats log message timestamps in utc
        dt = datetime.fromtimestamp(record.created, tz=timezone.utc)
        return dt.isoformat(timespec="milliseconds").replace("+00:00", "Z")


def setup_root_logger(log_level: int = logging.INFO):
    # The log format should probably be a constant, or should it be?
    formatter = Formatter(LOG_FORMAT)

    stream_handler = logging.StreamHandler(sys.stderr)
    stream_handler.setFormatter(formatter)
    # Handler doesn't need to filter log messages
    stream_handler.setLevel(logging.NOTSET)

    # Root logger setup
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(stream_handler)
