#!/usr/bin/env python3
# Copyright (c) 2021 Polytec GmbH, Waldbronn
# Released under the terms of the GNU Lesser General Public License version 3.

import setuptools

setuptools.setup(
    name="polytec-polytecgmbh",
    version="0.0.1",
    author="Matthias Cipold",
    author_email="mcipold@polytec.de",
    description="The general polytec package for public use",
    license="LGPLv3",
    classifiers=[
        "Programming Language :: Python :: 3",
        'Intended Audience :: Developers',
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: Microsoft :: Windows"
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.7",
    package_data={"": [
        "resources/DeviceCommunication32.dll",
        "resources/DeviceCommunication64.dll"
    ]}
)