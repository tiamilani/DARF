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
def apply_set(df: pd.DataFrame,
              ax: mplt.axes.Axes,
              ax_id: Optional[int] = None,
              *args, **kwargs) -> mplt.axes.Axes:
    """set.

    apply a generic `set` operatin to the ax matplotib object.
    (relevant matplotlib docs)[https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.set.html]

    Parameters
    ----------
    df : pd.DataFrame
        The input data, not used
    ax : mplt.axes.Axes
        The axis where to set the xlabel
    **kwargs : dict
        The kwargs to pass to the set method

    Returns
    -------
    mplt.axes.Axes
        The axis with the xlabel set
    """
    if ax_id is not None:
        current_ax = mplt.pyplot.gcf().axes[ax_id]
        current_ax.set(**kwargs)
    else:
        if len(mplt.pyplot.gcf().axes) == 1:
            ax.set(**kwargs)
        else:
            for current_ax in mplt.pyplot.gcf().axes:
                current_ax.set(**kwargs)
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
def tickparams(df: pd.DataFrame,
               ax: mplt.axes.Axes,
               *args, **kwargs) -> mplt.axes.Axes:
    """tickparams.

    Set the tick params

    Parameters
    ----------
    df : pd.DataFrame
        The input data
    ax : mplt.axes.Axes
        The axis where to set the tick params

    Returns
    -------
    mplt.axes.Axes
        The axis with the tick params set
    """
    ax.tick_params(*args, **kwargs)
    return ax

@plot_op
def set_ax(df: pd.DataFrame,
           ax: mplt.axes.Axes,
           ax_id: Optional[int] = None,
           row_id: Optional[int] = None,
           col_id: Optional[int] = None,
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
        The axis id, if not provided the operations will be applied
        to all the axes
    row_id: int
        The row id in case of multiple axes, the operations will be
        applied to all the axes in the row, applicable only on facetGrids
    col_id: int
        The column id in case of multiple axes, the operations will be
        applied to all the axes in the column, applicable only on facetGrids
    y_label : str
        The y label for the outage probability axis
    y_lim : tuple[float, float]
        The y limits for the outage probability axis

    Returns
    -------
    mplt.axes.Axes
        The axis with the outage probability set

    Raises
    ------
    AssertionError
        If the ax is not a FacetGrid and row_id or col_id are not None
    """
    axes = mplt.pyplot.gcf().axes
    selected_axes = axes if ax_id is None else [axes[ax_id]]

    if row_id is not None or col_id is not None:
        assert isinstance(ax, sns.FacetGrid), "FacetGrid is required"

        if row_id is not None and col_id is not None:
            selected_axes = ax.facet_axis(row_id, col_id)
        elif row_id is not None:
            selected_axes = ax.axes[row_id]
        elif col_id is not None:
            selected_axes = [ax.axes[i][col_id] for i in range(len(ax.axes))]

    for current_ax in selected_axes:
        if y_label is not None:
            current_ax.set_ylabel(y_label)

        current_ax.set_yticks(*y_ticks[0], **y_ticks[1])

        if y_lim is not None:
            current_ax.set_ylim(*y_lim)

        if remove_legend and current_ax.get_legend() is not None:
            current_ax.get_legend().remove()
    return ax