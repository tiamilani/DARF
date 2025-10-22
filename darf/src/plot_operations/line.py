# © 2025 Nokia
# Licensed under the BSD 3-Clause License
# SPDX-License-Identifier: BSD-3-Clause
#
# Contact: Mattia Milani (Nokia) <mattia.milani@nokia.com>

"""
Line plot operations
====================

All functions that can be applied to add lines to the plot
"""

from typing import Optional, List, Dict, Any

import datetime
import pandas as pd
import matplotlib as mplt

from darf.src.decorators import plot_op

def aggregate(df: pd.DataFrame,
              column: str,
              agg: str) -> float:
    """aggregate.

    Aggregate the data

    Parameters
    ----------
    df : pd.DataFrame
        The input data
    column : str
        The column to aggregate
    agg : str
        The aggregation method

    Returns
    -------
    float
        The aggregated value
    """
    match agg:
        case 'mean':
            return df[column].mean()
        case 'median':
            return df[column].median()
        case 'max':
            return df[column].max()
        case 'min':
            return df[column].min()
        case 'first':
            return df[column].iloc[0]
        case 'last':
            return df[column].iloc[-1]
        case 'plus_std':
            return df[column].mean() + df[column].std()
        case 'minus_std':
            return df[column].mean() - df[column].std()
        case _:
            raise ValueError(f"Data aggregation {agg} not supported")

@plot_op
def vertical_line(df: pd.DataFrame,
                  ax,
                  ax_id: int = 0,
                  from_clm: Optional[str] = None,
                  hue: Optional[str] = None,
                  hue_order: Optional[List[str]] = None,
                  data_agg: Optional[str] = None,
                  **kwargs):
    """vertical_line.

    Add a vertical line to the plot

    Parameters
    ----------
    df : pd.DataFrame
        The input data
    ax : mplt.axes.Axes
        The axis where to add the line

    Returns
    -------
    mplt.axes.Axes
        The axis with the line added
    """
    if from_clm is not None:
        if 'x' in kwargs:
            raise ValueError("x is already provided in kwargs, aggregation and 'x' column cannot be used together") # pylint: disable=line-too-long

        x = df.copy()
        if hue is not None:
            hue_order = hue_order if hue_order is not None else df[hue].unique()
            x = df[df[hue].isin(hue_order)].copy()
        x = aggregate(x, from_clm, data_agg)

        kwargs['x'] = x

    current_ax = mplt.pyplot.gcf().axes[ax_id]
    current_ax.axvline(**kwargs)
    return ax

@plot_op
def horizontal_line(df: pd.DataFrame,
                    ax,
                    ax_id: int = 0,
                    from_clm: Optional[str] = None,
                    hue: Optional[str] = None,
                    hue_order: Optional[List[str]] = None,
                    data_agg: Optional[str] = None,
                    **kwargs):
    """horizontal_line.

    Add a horizontal line to the plot

    Parameters
    ----------
    df : pd.DataFrame
        The input data
    ax : mplt.axes.Axes
        The axis where to add the line
    ax_id: int
        The axis id
    from_clm: str
        The column to group data for the line
    hue: str
        The hue column to slect the data if the dataset is in long format
    hue_order: list[str]
        The order of the hue, if not provided it will be the unique values of the hue column
    data_agg: str
        The aggregation method to apply to the data

    Returns
    -------
    mplt.axes.Axes
        The axis with the line added
    """
    if from_clm is not None:
        if 'y' in kwargs:
            raise ValueError("y is already provided in kwargs, aggregation and 'y' column cannot be used together") # pylint: disable=line-too-long

        y = df.copy()
        if hue is not None:
            hue_order = hue_order if hue_order is not None else df[hue].unique()
            y = df[df[hue].isin(hue_order)].copy()

        y = aggregate(y, from_clm, data_agg)
        kwargs['y'] = y

    current_ax = mplt.pyplot.gcf().axes[ax_id]
    current_ax.axhline(**kwargs)
    return ax

@plot_op
def add_outage_line(df: pd.DataFrame,
                    ax: mplt.axes.Axes,
                    ax_id: Optional[int] = None,
                    anomalies_column: Optional[str] = None,
                    anomalies_reference: Optional[str] = None,
                    ax_kwargs: Optional[dict] = None,
                    txt_flag: bool = True,
                    txt_kwargs: Optional[Dict[str, Any]] = None) -> mplt.axes.Axes:
    """add_outage_line.

    Add an outage line to the plot

    Parameters
    ----------
    df : pd.DataFrame
        The input data
    ax : mplt.axes.Axes
        The axis where to add the line
    anomalies_column: str
        column that contains the anomalies flag
    anomalies_reference: str
        column that contains the reference for the anomalies (datetime)
    ax_kwargs: dict,
        kwargs for the axvline
    txt_flag: bool
        flag to add the text to the line
    txt_kwargs: dict
        kwargs for the text

    Returns
    -------
    mplt.axes.Axes
        The axis with the line added
    """
    axes = mplt.pyplot.gcf().axes
    selected_axes = axes if ax_id is None else axes[ax_id]
    if anomalies_column is None:
        raise ValueError("Anomalies column is required")
    if anomalies_reference is None:
        raise ValueError("Anomalies reference is required")

    if ax_kwargs is None:
        ax_kwargs = {'color': 'red', 'linestyle': '--'}

    default_txt_kwargs = {'delta': {'minutes': 10},
                          'y': 0.8,
                          'format': '%H:%M'}
    if txt_kwargs is None:
        txt_kwargs = {}

    for key, item in default_txt_kwargs.items():
        if key not in txt_kwargs.keys():
            txt_kwargs[key] = item

    top_y = selected_axes.get_ylim()[1]
    delta = txt_kwargs['delta']
    y = txt_kwargs['y']
    time_format = txt_kwargs['format']
    del txt_kwargs['delta']
    del txt_kwargs['y']
    del txt_kwargs['format']
    for i in df[df[anomalies_column] == 1][anomalies_reference].unique():
        selected_axes.axvline(i, **ax_kwargs)

        if txt_flag:
            selected_axes.text(i+datetime.timedelta(**delta),
                    top_y*y,
                    f"{i.strftime(time_format)}",
                    **txt_kwargs)

    return ax

@plot_op
def add_circle(df: pd.DataFrame,
               ax: mplt.axes.Axes,
               *args,
               ax_id: int = 0,
               **kwargs) -> mplt.axes.Axes:
    """add_circle.
    Add a circle to the plot

    Parameters
    ----------
    df : pd.DataFrame
        The input data
    ax : mplt.axes.Axes
        The axis where to add the circle
    ax_id: int
        The axis id
    *args : tuple
        Additional positional arguments for the circle
    **kwargs : dict
        Additional keyword arguments for the circle

    Returns
    -------
    mplt.axes.Axes
        The axis with the circle added
    """
    current_ax = mplt.pyplot.gcf().axes[ax_id]
    print(current_ax.get_xlim())
    current_ax.add_patch(mplt.pyplot.Circle(*args, **kwargs))
    return ax

# TODO df should not be a mandatory argument for plot operation, while AX it should be, move df to
# kwargs
@plot_op
def add_ellipse(df: pd.DataFrame,
                ax: mplt.axes.Axes,
                *args,
                ax_id: int = 0,
                **kwargs) -> mplt.axes.Axes:
    """add_circle.
    Add an ellipse to the plot

    Parameters
    ----------
    df : pd.DataFrame
        The input data
    ax : mplt.axes.Axes
        The axis where to add the circle
    ax_id: int
        The axis id
    *args : tuple
        Additional positional arguments for the circle
    **kwargs : dict
        Additional keyword arguments for the circle

    Returns
    -------
    mplt.axes.Axes
        The axis with the circle added
    """
    current_ax = mplt.pyplot.gcf().axes[ax_id]
    current_ax.add_patch(mplt.patches.Ellipse(*args, **kwargs))
    return ax
