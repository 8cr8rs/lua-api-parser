# SPDX-FileCopyrightText: 2026 eightcraters <eightcraters@hotmail.com>
# SPDX-License-Identifier: Apache-2.0

from typing import override

from datetime import datetime, timezone
import logging


LOG_FORMAT = "[%(name)s] [%(levelname)s] [%(asctime)s] %(message)s"


class Formatter(logging.Formatter):
    @override
    def format(self, record: logging.LogRecord) -> str:
        # formats log level name as lowercase
        record.levelname = record.levelname.lower()
        return super().format(record)

    @override
    def formatTime(self, record: logging.LogRecord, datefmt: str | None = None) -> str:
        # formats log message timestamps in utc
        dt = datetime.fromtimestamp(record.created, tz=timezone.utc)
        return dt.isoformat(timespec="milliseconds").replace("+00:00", "Z")


def get_logger(name: str, log_level: int = logging.INFO) -> logging.Logger:
    # formatter
    formatter = Formatter(LOG_FORMAT)

    # streamhandler setup
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    # handler doesn't need to filter log messages
    stream_handler.setLevel(logging.NOTSET)

    # logger setup
    logger = logging.getLogger(name)
    logger.addHandler(stream_handler)
    logger.setLevel(log_level)

    return logger
