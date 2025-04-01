# © 2025 Nokia
# Licensed under the BSD 3-Clause License
# SPDX-License-Identifier: BSD-3-Clause
#
# Contact: Mattia Milani (Nokia) <mattia.milani@nokia.com>

"""
Environment conf module
=======================

Module used to configure the main environment points like
RNG and others.

"""

import os

from darf.src.io import Pb as pb
from darf.src.params import ParamHandler as Par
from darf.src.decorators import f_logger

def set_tensorflow_device(device: str):
    """set_tensorflow_device.

    This is an exclusive setter, so it excludes the usage
    of GPU or CPU devices.

    Parameters
    ----------
    device : str
        device to keep active, if CPU is passed then GPU
        devices are excluded and viceversa.
    """
    match device:
        case "GPU":
            os.environ['CUDA_VISIBLE_DEVICES'] = '0'
        case "CPU":
            os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
        case _:
            raise ValueError(f"Unknown device {device}")

@f_logger
def conf(params: Par, **kwargs):
    """conf.

    Parameters
    ----------
    params : Par
        params
    args :
        args
    kwargs :
        kwargs
    """
    _, write_msg = kwargs["logger"], kwargs["write_msg"]
    del kwargs["logger"]
    del kwargs["write_msg"]

    pbar = pb.databar(len(params.objects.keys()), desc="Loading environment ...")

    for key, param in params.objects.items():
        match key:
            case "tensorflow_device":
                set_tensorflow_device(param.value)
            case _:
                write_msg(f"Unknown parameter {key}")
                raise ValueError(f"Unknown environment parameter {key}")
        pbar.update(1)

    pb.success_close(pbar, "Environment loaded")

