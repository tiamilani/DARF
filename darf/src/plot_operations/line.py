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

from typing import Optional, List

import pandas as pd
import matplotlib as mplt
import datetime
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
                  ax: mplt.axes.Axes,
                  ax_id: int = 0,
                  from_clm: Optional[str] = None,
                  hue: Optional[str] = None,
                  hue_order: Optional[List[str]] = None,
                  data_agg: Optional[str] = None,
                  **kwargs) -> mplt.axes.Axes:
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
            raise ValueError("x is already provided in kwargs, aggregation and 'x' column cannot be used together")

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
                    ax: mplt.axes.Axes,
                    ax_id: int = 0,
                    from_clm: Optional[str] = None,
                    hue: Optional[str] = None,
                    hue_order: Optional[List[str]] = None,
                    data_agg: Optional[str] = None,
                    **kwargs) -> mplt.axes.Axes:
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
            raise ValueError("y is already provided in kwargs, aggregation and 'y' column cannot be used together")

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
                    anomalies_column: Optional[str] = None,
                    anomalies_reference: Optional[str] = None,
                    ax_kwargs: Optional[dict] = None,
                    txt_flag: bool = True,
                    txt_kwargs: Optional[dict] = None,
                    **kwargs) -> mplt.axes.Axes:
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
    **kwargs :
        kwargs applied to the axvline

    Returns
    -------
    mplt.axes.Axes
        The axis with the line added
    """
    if anomalies_column is None:
        raise ValueError("Anomalies column is required")
    if anomalies_reference is None:
        raise ValueError("Anomalies reference is required")

    if ax_kwargs is None:
        ax_kwargs = {'color': 'red', 'linestyle': '--'}

    default_txt_kwargs = {'delta': {'minutes': 10},
                          'y': 0.8,
                          'format': '%H:%M'}
    if txt_kwargs is not None:
        default_txt_kwargs.update(txt_kwargs)
        for key in default_txt_kwargs.keys():
            if key in txt_kwargs:
                del txt_kwargs[key]

    top_y = ax.get_ylim()[1]
    for i in df[df[anomalies_column] == 1][anomalies_reference].unique():
        ax.axvline(i, **ax_kwargs)

        if txt_flag:
            delta = default_txt_kwargs['delta']
            y = default_txt_kwargs['y']
            time_format = default_txt_kwargs['format']

            ax.text(i+datetime.timedelta(**delta),
                    top_y*y,
                    f"{i.strftime(time_format)}",
                    **txt_kwargs)

    return ax
