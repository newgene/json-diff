#!/usr/bin/env python
# coding=utf-8
import os
import os.path

"""
constant
"""

GZPACKAGE_DIR = './gzpackages'
EXTRACTED_DIR = './db'
#EXTRACTED_DIR = './gzextract'
CSVFILES_DIR = './csvfiles'
LOG = './log.csv'

def makeDir(directory):
    """
    if the directory do not exists, make it.
    """
    have_dir = os.path.exists(directory)
    if not have_dir:
        os.makedirs(directory)
