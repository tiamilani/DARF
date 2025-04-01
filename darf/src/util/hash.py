# © 2025 Nokia
# Licensed under the BSD 3-Clause License
# SPDX-License-Identifier: BSD-3-Clause
#
# Contact: Mattia Milani (Nokia) <mattia.milani@nokia.com>

"""
Hash module
===========

Use this module to manage and get access to hashes of
objects.
"""

from hashlib import blake2b

def compute_hash(obj: str, *args,
                 encoding: str = "utf-8",
                 **kwargs) -> str:
    """compute_hash.

    Use library blake2 to compute the hash of the input

    Parameters
    ----------
    obj : str
        obj String representation fo the object
    args :
        args
    kwargs :
        kwargs

    Returns
    -------
    str
    """
    return blake2b(obj.encode(encoding), *args, **kwargs).hexdigest()
