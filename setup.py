#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 15:40:54 2017

@author: koolok
"""

from distutils.core import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize("distanceC.pyx")
)