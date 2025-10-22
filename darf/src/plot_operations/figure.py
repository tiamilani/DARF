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

from typing import Optional, List

import pandas as pd
import matplotlib as mplt

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

@plot_op
def set_font_size(df: pd.DataFrame,
                  ax: mplt.axes.Axes,
                  *args,
                  ax_id: Optional[int] = None,
                  items: Optional[List[str]] = None,
                  **kwargs) -> mplt.axes.Axes:
    """set_font_size.

    Set the font size of the figure

    Parameters
    ----------
    df : pd.DataFrame
        The input data
    ax : mplt.axes.Axes
        The axis where to set the font size
    ax_id : int
        The axis id
    items : list
        The items to set the font size, list can contain the following
        elements: Title, XLabel, YLabel, XTicks, YTicks
    args :
        The font size args
    kwargs :
        The font size kwargs

    Returns
    -------
    mplt.axes.Axes
        The axis with the font size set

    Raises
    ------
    ValueError
        If the item is not recognized
    """
    axes = mplt.pyplot.gcf().axes
    apply_axes = axes if ax_id is None else [axes[ax_id]]

    def get_all_items(current_ax: mplt.axes.Axes):
        return [current_ax.title,
                current_ax.xaxis.label,
                current_ax.yaxis.label] +\
               current_ax.get_xticklabels() +\
               current_ax.get_yticklabels()

    def get_selected_items(current_ax: mplt.axes.Axes):
        selected_items = []
        for item in items:
            match item:
                case "Title":
                    selected_items.append(current_ax.title)
                case "XLabel":
                    selected_items.append(current_ax.xaxis.label)
                case "YLabel":
                    selected_items.append(current_ax.yaxis.label)
                case "XTicks":
                    selected_items += current_ax.get_xticklabels()
                case "YTicks":
                    selected_items += current_ax.get_yticklabels()
                case _:
                    raise ValueError(f"Item {item} not recognized")
        return selected_items

    for current_ax in apply_axes:
        selected_items = get_all_items(current_ax) if items is None \
                            else get_selected_items(current_ax)

        for item in selected_items:
            item.set_fontsize(*args, **kwargs)

    return ax

@plot_op
def set_size_inches(df: pd.DataFrame,
                    ax: mplt.axes.Axes,
                    width: Optional[float] = None,
                    height: Optional[float] = None,
                    **kwargs) -> mplt.axes.Axes:
    """set_size_inches.

    Set the size of the figure in inches

    Parameters
    ----------
    df : pd.DataFrame
        The input data
    ax : mplt.axes.Axes
        The axis where to set the size
    width : float
        The width of the figure
    height : float
        The height of the figure
    kwargs :
        The size kwargs

    Returns
    -------
    mplt.axes.Axes
        The axis with the size set
    """
    current_figure = mplt.pyplot.gcf()
    width = width if width is not None else current_figure.get_figwidth()
    height = height if height is not None else current_figure.get_figheight()
    current_figure.set_size_inches(width, height, **kwargs)
    return ax
