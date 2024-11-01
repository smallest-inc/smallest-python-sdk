# Copyright 2023-2024 Python SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from setuptools import setup, find_packages
import os.path
import sys

if sys.version_info < (3, 9):
    sys.exit("Sorry, Python < 3.9 is not supported")

with open("README.md", "r", encoding="utf-8") as fh:
    LONG_DESCRIPTION = fh.read()

DESCRIPTION = (
    "The official Python SDK for the Smallest AI TTS platform."
)

setup(
    name="smallest-python",
    author="Smallest",
    author_email="info@smallest.ai",
    url="https://github.com/smallest-inc/smallest-python",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    license="MIT",
    packages=find_packages(exclude=["tests"]),
    install_requires=[
        "aiohttp",
        "aiofiles",
        "requests",
        "num2words",
        "sacremoses",
        "pydub",
        "websockets",
        "websocket-client"
    ],
    keywords=["smallest", "smallest.ai", "tts", "text-to-speech"],
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
)
