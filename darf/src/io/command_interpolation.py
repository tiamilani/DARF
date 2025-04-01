# © 2025 Nokia
# Licensed under the BSD 3-Clause License
# SPDX-License-Identifier: BSD-3-Clause
#
# Contact: Mattia Milani (Nokia) <mattia.milani@nokia.com>

"""
Commands Interpolation Module
=============================

This module contains the command interpolation methods
that should been called when a command is required
inside an interpolation

"""

import re
from datetime import datetime as DT

from darf.src.decorators import interpolate_functions, interpolator

@interpolator
def datetime(*args, **kwargs) -> str:
    """datetime.
    Get the current date and time in the format dd-mm-YYYY_HH-MM-SS

    Parameters
    ----------
    args :
        args
    kwargs :
        kwargs

    Returns
    -------
    str

    """
    return DT.now().strftime('%d-%m-%Y_%H-%M-%S', *args, **kwargs)

@interpolator
def date(*args, **kwargs) -> str:
    """date.
    Get the current date in the format dd-mm-YYYY

    Parameters
    ----------
    args :
        args
    kwargs :
        kwargs

    Returns
    -------
    str

    """
    return DT.now().strftime('%d-%m-%Y', *args, **kwargs)

def fn(function, *args, **kwargs):
    """fn.
    Identifies the requested interpolation function ans substitutes with
    the value returned by the function

    Parameters
    ----------
    function :
        function
    args :
        args
    kwargs :
        kwargs
    """
    if isinstance(function, re.Match):
        function = function.group(0)
        function = function.replace("{", "")
        function = function.replace("}", "")

    if not isinstance(function, str) or \
        function[0] != "!" or \
        not function[1::] in interpolate_functions:
        raise ValueError(f"Command \"{function}\" not available remember to escape \
                the commands with a '!'")
    return interpolate_functions[function[1::]](*args, **kwargs)

def str_interpolate(s: str, pattern: str = r"\{[^\}]*\}") -> str:
    """str_interpolate.
    Interpolate a string with the given pattern
    using regex.sub

    Parameters
    ----------
    s : str
        s
    pattern : str
        pattern

    Returns
    -------
    str

    """
    return re.sub(pattern, fn, s)
