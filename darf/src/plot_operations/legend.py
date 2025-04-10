# © 2025 Nokia
# Licensed under the BSD 3-Clause License
# SPDX-License-Identifier: BSD-3-Clause
#
# Contact: Mattia Milani (Nokia) <mattia.milani@nokia.com>

"""
Legend plot operations
======================

All functions that can be applied to add custom legends
"""

from typing import Optional, List, Dict, Any

import pandas as pd
import matplotlib as mplt
from matplotlib.lines import Line2D
from darf.src.decorators import plot_op

def legend_line(*args, **kwargs) -> Line2D:
    """legend_line.

    Create a custom legend line

    Parameters
    ----------
    args :
        args
    kwargs :
        kwargs

    Returns
    -------
    Line2D
    """
    return Line2D(*args, **kwargs)

@plot_op
def legend(df: pd.DataFrame,
           ax: mplt.axes.Axes,
           ax_id: int = 0,
           handles: Optional[List[Dict[str, Any]]] = None,
           **kwargs) -> mplt.axes.Axes:
    """legend.

    Add a legend to the plot

    Parameters
    ----------
    df : pd.DataFrame
        The input data
    ax : mplt.axes.Axes
        The axis where to add the legend
    ax_id: int
        The axis id in case multiple axes are in the same figure
    handles : List[Dict[str, Any]]
        The handles to add to the legend if None no custom handles will
        be generated

    Returns
    -------
    mplt.axes.Axes
        The axis with the legend added
    """
    custom_handles = []
    for handle in handles:
        handle_type = handle.get('type', None)
        match handle_type:
            case "Line2D":
                custom_handles.append(legend_line(*handle['args'], **handle['kwargs']))
            case "Patch":
                custom_handles.append(mplt.patches.Patch(**handle['kwargs']))
            case _:
                raise ValueError(f"Unknown handle key {handle_type}")

    if 'handles' not in kwargs and handles is not None:
        kwargs['handles'] = custom_handles

    selected_ax = mplt.pyplot.gcf().axes[ax_id]
    selected_ax.legend(**kwargs)
    return ax

@plot_op
def legend_z_order(df: pd.DataFrame,
                   ax: mplt.axes.Axes,
                   ax_id: int = 0,
                   zorder: int = 10) -> mplt.axes.Axes:
    selected_ax = mplt.pyplot.gcf().axes[ax_id]
    selected_ax.get_legend().set_zorder(zorder)
    return ax

@plot_op
def remove_legend(df: pd.DataFrame,
                  ax: mplt.axes.Axes,
                  ax_id: Optional[int] = None) -> mplt.axes.Axes:
    if ax_id is None:
        for selected_ax in mplt.pyplot.gcf().axes:
            if selected_ax.get_legend() is not None:
                selected_ax.get_legend().remove()
    else:
        selected_ax = mplt.pyplot.gcf().axes[ax_id]
        selected_ax.get_legend().remove()
    return ax
