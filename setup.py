#!/usr/bin/python3

from setuptools import setup

setup(
    name="pynit",
    version="1.0",
    install_requires=["numpy"],
    packages=["pynit"],
    package_data={'': ['libs/*']},
    python_requires=">=3.8",
)
