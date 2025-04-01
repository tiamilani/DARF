# © 2025 Nokia
# Licensed under the BSD 3-Clause License
# SPDX-License-Identifier: BSD-3-Clause
#
# Contact: Mattia Milani (Nokia) <mattia.milani@nokia.com>

"""
Module contextManagers
======================

This module is used to collect the context managers that can be used
"""

from time import time
from contextlib import contextmanager
from darf.src.decorators import f_logger

from darf.src.log import LogHandler

@contextmanager
@f_logger
def timeit_cnt(name, **kwargs):
    """timeit_cnt.

    Context manager to measure the time of a context

    Parameters
    ----------
    name :
        name to give the context, this name will then be used to log the
        information to STDOUT or to a file if logger has been passed
    kwargs :
        kwargs
    """
    _, write_msg = kwargs["logger"], kwargs["write_msg"]
    del kwargs["logger"]
    del kwargs["write_msg"]

    start_time = time()
    yield
    delta_t = time() - start_time
    write_msg(f"Context {name} finished in {int(delta_t*1000)} ms", LogHandler.DEBUG)
    print(f"Context {name} finished in {int(delta_t*1000)} ms")
