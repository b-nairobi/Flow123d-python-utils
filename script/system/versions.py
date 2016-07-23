#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs
"""
" This work is a derivative of "Flow123d-python-utils"
" (https://github.com/x3mSpeedy/Flow123d-python-utils) by Jan Hybš, used
" under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/).
" This work is licensed under CC BY 4.0 by b.nairobi.dev+gh@gmail.com.
"""

"""
Simple module which provides method for testing running python version
"""

import sys


def require_version_2 ():
    """requires version higher than 3"""
    if sys.version_info > (3, 0):
        print ('Error: Python 2 is required')
        sys.exit (1)


def require_version_3 ():
    """requires version lower than 3"""
    if sys.version_info < (3, 0):
        print ('Error: Python 3 is required')
        sys.exit (1)
