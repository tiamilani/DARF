# © 2025 Nokia
# Licensed under the BSD 3-Clause License
# SPDX-License-Identifier: BSD-3-Clause
#
# Contact: Mattia Milani (Nokia) <mattia.milani@nokia.com>

"""
Figure plot operations
======================

Adjust figure level elements
"""

from typing import Optional, Dict, Tuple

import pandas as pd
import matplotlib as mplt
import matplotlib.dates as mdates

from darf.src.decorators import plot_op

@plot_op
def set_title(df: pd.DataFrame,
              ax: mplt.axes.Axes,
              ax_id: int = 0,
              **kwargs) -> mplt.axes.Axes:
    """set_title.

    Set the title of the figure

    Parameters
    ----------
    df : pd.DataFrame
        The input data
    ax : mplt.axes.Axes
        The axis where to set the title
    ax_id : int
        The axis id
    kwargs :
        The title kwargs

    Returns
    -------
    mplt.axes.Axes
        The axis with the title set
    """
    current_ax = mplt.pyplot.gcf().axes[ax_id]
    current_ax.set_title(**kwargs)
    return ax

@plot_op
def set_xlabel(df: pd.DataFrame,
               ax: mplt.axes.Axes,
               ax_id: int = 0,
               **kwargs) -> mplt.axes.Axes:
    """set_xlabel.

    Set the x label of the figure

    Parameters
    ----------
    df : pd.DataFrame
        The input data
    ax : mplt.axes.Axes
        The axis where to set the x label
    ax_id : int
        The axis id
    kwargs :
        The x label kwargs

    Returns
    -------
    mplt.axes.Axes
        The axis with the x label set
    """
    current_ax = mplt.pyplot.gcf().axes[ax_id]
    current_ax.set_xlabel(**kwargs)
    return ax

@plot_op
def set_ylabel(df: pd.DataFrame,
               ax: mplt.axes.Axes,
               ax_id: int = 0,
               **kwargs) -> mplt.axes.Axes:
    """set_ylabel.

    Set the y label of the figure

    Parameters
    ----------
    df : pd.DataFrame
        The input data
    ax : mplt.axes.Axes
        The axis where to set the y label
    ax_id : int
        The axis id
    kwargs :
        The y label kwargs

    Returns
    -------
    mplt.axes.Axes
        The axis with the y label set
    """
    current_ax = mplt.pyplot.gcf().axes[ax_id]
    current_ax.set_ylabel(**kwargs)
    return ax
