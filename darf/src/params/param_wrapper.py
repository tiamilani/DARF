# © 2025 Nokia
# Licensed under the BSD 3-Clause License
# SPDX-License-Identifier: BSD-3-Clause
#
# Contact: Mattia Milani (Nokia) <mattia.milani@nokia.com>

"""
paramWrapper Module
===================

Used to wrap and manage different parameters types
"""


from darf.src.data_operations import OP_caller
from darf.src.plot_operations import PLT_OP_caller
from darf.src.util.strings import s
from darf.src.decorators import cls_wrapper, classes

from .parameters import _param, TypeSpecific, CallableParam, Dataset, Plot

@cls_wrapper
def generic(*args, **kwargs) -> _param:
    """generic.

    Parameters
    ----------
    args :
        args
    kwargs :
        kwargs

    Returns
    -------
    _param

    """
    return _param(*args, **kwargs)

@cls_wrapper
def dataset(*args, **kwargs) -> Dataset:
    """dataset.

    Parameters
    ----------
    args :
        args
    kwargs :
        kwargs

    Returns
    -------
    Dataset

    """
    return Dataset(*args, **kwargs)

@cls_wrapper
def operation(*args, **kwargs) -> CallableParam:
    """operation.

    Parameters
    ----------
    args :
        args
    kwargs :
        kwargs

    Returns
    -------
    Callable

    """
    return CallableParam(*args, function=OP_caller,
                            param_type=s.param_op_type, **kwargs)

@cls_wrapper
def plot_operation(*args, **kwargs) -> CallableParam:
    """plot_operations.

    Parameters
    ----------
    args :
        args
    kwargs :
        kwargs

    Returns
    -------
    Callable

    """
    return CallableParam(*args, function=PLT_OP_caller,
                            param_type=s.param_plot_op_type, **kwargs)

@cls_wrapper
def plot(*args, **kwargs) -> Plot:
    """plot.

    Parameters
    ----------
    args :
        args
    kwargs :
        kwargs

    Returns
    -------
    Plot

    """
    return Plot(*args, **kwargs)

@cls_wrapper
def environment(*args, **kwargs) -> TypeSpecific:
    """environment.

    Parameters
    ----------
    args :
        args
    kwargs :
        kwargs

    Returns
    -------
    TypeSpecific

    """
    return TypeSpecific(*args, param_type=s.env_par, **kwargs)

def param_selector(obj, *args, **kwargs):
    """param_selector.

    Parameters
    ----------
    obj :
        obj
    args :
        args
    kwargs :
        kwargs
    """
    if obj not in classes:
        raise ValueError(f"Class {obj} not found in availabel params")
    return classes[obj](*args, **kwargs)
