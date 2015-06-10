#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from setuptools import setup


def read_req(filename):
    return open(filename).read().split()


setup(
    name="graphql",
    version="0.0.1",
    url='https://github.com/lsmag/graphql',
    author='Lucas Sampaio',
    author_email='lucas@lsmagalhaes.com',
    description='Python implementation of GraphQL markup language',
    include_package_data=True,
    install_requires=read_req('requirements.txt'),
    tests_require=read_req('dev_requirements.txt'),
    license="Apache 2.0",
)
