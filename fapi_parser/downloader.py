# SPDX-FileCopyrightText: 2026 eightcraters <eightcraters@hotmail.com>
# SPDX-License-Identifier: Apache-2.0

from zipfile import ZipFile

import requests
from requests.exceptions import HTTPError

BASE_URL = "https://lua-api.factorio.com"

# todo: rename the a_* functions

def a_1(version: str) -> bool:
    """Checks if a version exists"""
    try:
        response = requests.head(f"{BASE_URL}/{version}")
        response.raise_for_status()
        return True
    except HTTPError:
        if e.response.status_code == 404:
            return False
        # raise to higher caller if some other error occurs
        raise


def a_2(version: str, file_path: str) -> None:
    """Downloads the archive.zip from a specific version"""
    try:
        response = requests.get(f"{BASE_URL}/{version}/static/archive.zip")
        response.raise_for_status()
        with open(file_path, "bw") as f:
            _ = f.write(response.content)
    except HTTPError:
        pass


def a_3(zip_path: str, dest: str) -> None:
    with ZipFile(zip_path, "r") as zip:
        zip.extractall(dest)


def main():
    pass


if __name__ == "__main__":
    print(main())
