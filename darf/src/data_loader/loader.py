# © 2025 Nokia
# Licensed under the BSD 3-Clause License
# SPDX-License-Identifier: BSD-3-Clause
#
# Contact: Mattia Milani (Nokia) <mattia.milani@nokia.com>

"""
Loader module
=============

Use this module to abstract the loader class complexity.
"""

from typing import Any

from darf.src.decorators import data_loaders

def cls_loader(cls_name: str, *args, **kwargs) -> Any:
    """function_caller.
    Function to call the data loader class.
    Single ingress point for the loader classes

    Parameters
    ----------
    cls_name: str
        The class to call
    args : List
        List of arguments to pass to the function
    kwargs : Dict
        Dictionary of keyword arguments to pass to the function

    Returns
    -------
    Any
        The result of the function
    """
    if not isinstance(cls_name, str) or \
            not cls_name in data_loaders:
        raise ValueError(f"Class \"{cls_name}\" not available, \
                current available cls_names: {list(data_loaders.keys())}")
    return data_loaders[cls_name](*args, **kwargs)
