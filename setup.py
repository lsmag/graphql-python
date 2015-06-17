#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from setuptools import setup


def read_req(filename):
    return open(filename).read().split()


setup(
    name="graphql-python",
    version="0.0.1",
    url='https://github.com/lsmag/graphql-python',
    author='Lucas Sampaio',
    author_email='lucas@lsmagalhaes.com',
    description='Python implementation of GraphQL markup language',
    packages=['graphql'],
    include_package_data=True,
    install_requires=read_req('requirements.txt'),
    tests_require=read_req('dev_requirements.txt'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.0",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Intended Audience :: Developers",
        "Topic :: Text Processing :: Markup",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License"
    ]
)
