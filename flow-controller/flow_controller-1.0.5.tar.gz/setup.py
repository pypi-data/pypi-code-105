#!/usr/bin/env python
# coding: utf-8

import os
import setuptools

setuptools.setup(
    name='flow_controller',
    version='1.0.5',
    author='Ignace Konig',
    description='package for managing pipelines with simple commands',
    license='MIT',
    install_requires=['keyboard'],
    packages=setuptools.find_packages())

