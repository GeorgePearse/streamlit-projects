#!/usr/bin/env python

import os
from setuptools import setup

with open("./README.md") as fh:
    long_description = fh.read()

with open("./requirements.txt") as f:
    requirements = f.readlines()

# Got to make sure you delete previous build packages
# https://www.geeksforgeeks.org/command-line-scripts-python-packaging/
setup(
    name="streamlit-business-intelligence",
    version="0.0.3",
    description="Python library for SQL Data Analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GeorgePearse/streamlit-projects/tree/master/streamlit-bi",
    author="George Pearse",
    author_email="georgehwp26@gmail.com",
    license="MIT",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "streamlit-business-intelligence = src.streamlit_business_intelligence:main",
        ],
    },
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 3 - Alpha",
        # Indicate who your project is intended for
        "Intended Audience :: Developers",
        "Topic :: Software Development",
        # Pick your license as you wish (should match "license" above)
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        "Programming Language :: Python :: 3.6",
    ],
)
