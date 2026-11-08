# SPDX-FileCopyrightText: 2026 eightcraters <eightcraters@hotmail.com>
# SPDX-License-Identifier: Apache-2.0

import logging

import pytest

from fapi_parser import output


@pytest.fixture()
def formatter() -> logging.Formatter:
    return output.Formatter()

@pytest.fixture()
def log_record() -> logging.LogRecord:
    return logging.LogRecord(
        name="example",
        level=logging.INFO,
        pathname="",
        lineno=100,
        msg="Hello",
        args=(),
        exc_info=None
    )


@pytest.mark.skip
@pytest.mark.parametrize(
    "record, expected",
    []
)
def test_format(
    formatter: output.Formatter,
    record: logging.LogRecord,
    expected: str
) -> None:
    formatter.format(record)
    assert record.levelname == expected

@pytest.mark.skip
@pytest.mark.parametrize(
    "record, expected",
    []
)
def test_format_time(
    formatter: output.Formatter,
    record: logging.LogRecord,
    expected: str
) -> None:
    formatted_time = formatter.formatTime(record)
    assert formatted_time == expected
