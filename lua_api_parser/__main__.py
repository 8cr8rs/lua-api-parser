#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2026 eightcraters <eightcraters@hotmail.com>
# SPDX-License-Identifier: Apache-2.0

import sys

if not __package__ and not hasattr(sys, "frozen"):
    import os

    path = os.path.realpath(os.path.abspath(__file__))
    sys.path.insert(0, os.path.dirname(os.path.dirname(path)))

import lua_api_parser

if __name__ == "__main__":
    lua_api_parser.main()
