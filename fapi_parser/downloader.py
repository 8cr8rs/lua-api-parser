# SPDX-FileCopyrightText: 2026 eightcraters <eightcraters@hotmail.com>
# SPDX-License-Identifier: Apache-2.0

import logging
from zipfile import ZipFile

import requests
from requests.exceptions import HTTPError
from pathlib import Path

BASE_URL = "https://lua-api.factorio.com"

logger = logging.getLogger(__name__)


def check_version_exists(version: str) -> bool:
    """Checks if a version exists"""
    status_code = None
    try:
        logger.debug(f"Retrieving {version} from {BASE_URL}")
        response = requests.head(f"{BASE_URL}/{version}")
        status_code = response.status_code
        logger.debug(f"Got status code: {status_code}")
        response.raise_for_status()
        return True
    except HTTPError:
        if status_code == 404:
            return False
        # raise to higher caller if some other error occurs
        raise


def get_archive_zip(version: str, file_path: Path):
    """Downloads the archive.zip from a specific version"""
    try:
        zip_url = f"{BASE_URL}/{version}/static/archive.zip"
        logger.debug(f"Getting zip from {zip_url}")
        response = requests.get(zip_url)
        logger.debug(f"Got status code: {response.status_code}")
        response.raise_for_status()
        with open(file_path, "bw") as f:
            _ = f.write(response.content)
    except HTTPError:
        pass


def extract_zip(zip_path: Path, dest: Path):
    logger.debug(f"Extracting {zip_path} to {dest}")
    with ZipFile(zip_path, "r") as zip:
        zip.extractall(dest)
