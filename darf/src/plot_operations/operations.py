# © 2025 Nokia
# Licensed under the BSD 3-Clause License
# SPDX-License-Identifier: BSD-3-Clause
#
# Contact: Mattia Milani (Nokia) <mattia.milani@nokia.com>

"""
Plot operations Module
======================

This module contains all the functions that can be used to manipulate plot as a
sequence of operations.
From simple to complex and very context specific functions.
For context/experiment specific function define those in their specific
file and import it.

"""

from typing import Any

from darf.src.decorators import plot_operations

def function_caller(function: str, *args, **kwargs) -> Any:
    """function_caller.
    Function to call the plot operation functions.
    Single ingress point for the operation functions

    Parameters
    ----------
    function : str
        The function to call
    args : List
        List of arguments to pass to the function
    kwargs : Dict
        Dictionary of keyword arguments to pass to the function

    Returns
    -------
    Any
        The result of the function
    """
    if not isinstance(function, str) or \
            not function in plot_operations:
        raise ValueError(f"Plot Operation \"{function}\" not available, current available \
                functions: {list(plot_operations.keys())}")
    return plot_operations[function](*args, **kwargs)
