# © 2025 Nokia
# Licensed under the BSD 3-Clause License
# SPDX-License-Identifier: BSD-3-Clause
#
# Contact: Mattia Milani (Nokia) <mattia.milani@nokia.com>

"""
Axis plot operations
====================

Adjust x and y axis
"""

from typing import Optional, Dict, Tuple, List, Union, Any

import pandas as pd
import matplotlib as mplt
import matplotlib.dates as mdates

from darf.src.decorators import plot_op

@plot_op
def x_date_formatter(df: pd.DataFrame,
                     ax: mplt.axes.Axes,
                     date_format: Optional[str] = "%d-%b",
                     hour_locator_kwargs: Optional[dict] = None) -> mplt.axes.Axes:
    """x_date_formatter.

    Apply a date formatter to the x axis

    Parameters
    ----------
    df : pd.DataFrame
        The input data
    ax : mplt.axes.Axes
        The axis where to apply the date formatter
    date_format : str
        The date format to apply
    hour_locator_kwargs : dict
        The hour locator kwargs

    Returns
    -------
    mplt.axes.Axes
        The axis with the date formatter applied
    """
    mplt.pyplot.gca().xaxis.set_major_formatter(mdates.DateFormatter(date_format))
    mplt.pyplot.gca().xaxis.set_major_locator(mdates.HourLocator(**hour_locator_kwargs))
    ax.figure.autofmt_xdate()
    return ax

@plot_op
def set_xticks(df: pd.DataFrame,
               ax: mplt.axes.Axes,
               *args, **kwargs) -> mplt.axes.Axes:
    """set_xticks.

    Set the xticks

    Parameters
    ----------
    df : pd.DataFrame
        The input data
    ax : mplt.axes.Axes
        The axis where to set the xticks

    Returns
    -------
    mplt.axes.Axes
        The axis with the xticks set
    """
    ax.set_xticks(*args, **kwargs)
    return ax

@plot_op
def set_ax(df: pd.DataFrame,
           ax: mplt.axes.Axes,
           ax_id: int = 0,
           y_label: Optional[str] = None,
           y_lim: Optional[Tuple[float, float]] = None,
           y_ticks: List[Union[Tuple[float], Dict[str, Any]]] = [(0, 1.0),
                                                                 {'labels': [0, 100]}],
           remove_legend: bool = True
           ) -> mplt.axes.Axes:
    """set_ax.

    Set the ax properties

    Parameters
    ----------
    df : pd.DataFrame
        The input data
    ax : mplt.axes.Axes
        The axis where to set the outage probability
    ax_id : int
        The axis id for the outage probability
    y_label : str
        The y label for the outage probability axis
    y_lim : tuple[float, float]
        The y limits for the outage probability axis

    Returns
    -------
    mplt.axes.Axes
        The axis with the outage probability set
    """
    current_ax = mplt.pyplot.gcf().axes[ax_id]
    if y_label is not None:
        current_ax.set_ylabel(y_label)

    current_ax.set_yticks(*y_ticks[0], **y_ticks[1])

    if y_lim is not None:
        current_ax.set_ylim(*y_lim)

    if remove_legend and current_ax.get_legend() is not None:
        current_ax.get_legend().remove()
    return ax
