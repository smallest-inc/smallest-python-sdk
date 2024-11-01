# Copyright 2023-2024 Deepgram SDK contributors. All Rights Reserved.
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
        "httpx>=0.25.2",
        "websockets>=12.0",
        "dataclasses-json>=0.6.3",
        "typing_extensions>=4.9.0",
        "aiohttp>=3.9.1",
        "aiofiles>=23.2.1",
        "aenum>=3.1.0",
        "deprecation>=2.1.0",
    ],
    keywords=["smallest", "smallest.ai", "tts", "text-to-speech"],
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
)
