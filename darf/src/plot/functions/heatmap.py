# © 2025 Nokia
# Licensed under the BSD 3-Clause License
# SPDX-License-Identifier: BSD-3-Clause
#
# Contact: Mattia Milani (Nokia) <mattia.milani@nokia.com>

"""
Heatmap plot functions module
=============================

This module contains the heatmap plot functions that can be used to create a figure.
"""

from typing import Any, Dict, Optional
import pandas as pd
import seaborn as sns
import matplotlib as mplt
from darf.src.decorators.decorators import plot

@plot
def draw_heatmap(pvt_kwargs=None, htm_kwargs=None,
                 data: pd.DataFrame = None,
                 extract_rectangular: bool = False,
                 **kwargs) -> mplt.axes.Axes:
    """draw_heatmap.

    Apply a heatmap to the data and also pivot the dataset

    Parameters
    ----------
    pvt_kwargs :
        pvt_kwargs
    htm_kwargs :
        htm_kwargs
    kwargs :
        kwargs
    """

    # If the palette kwarg is present then remove it
    if 'palette' in kwargs:
        kwargs.pop('palette')

    tmp_df = data.copy()
    if extract_rectangular:
        new_values = []
        for row in tmp_df.iterrows():
            value = row[1][pvt_kwargs['values']]
            new_values.append(value.split('%')[0])
        tmp_df[pvt_kwargs['values']] = new_values
        tmp_df[pvt_kwargs['values']] = tmp_df[pvt_kwargs['values']].astype(float)

    if extract_rectangular:
        pivot_data = tmp_df.pivot(**pvt_kwargs)
        labels = data.pivot(**pvt_kwargs).reset_index(drop=True)
        labels = labels.astype(str)
    else:
        pivot_data = data.pivot(**pvt_kwargs)
        labels = data.pivot(**pvt_kwargs)


    if extract_rectangular:
        return sns.heatmap(data=pivot_data, annot=labels, **htm_kwargs, **kwargs)
    return sns.heatmap(data=pivot_data, **htm_kwargs, **kwargs)


@plot
def heatplot(data: Optional[pd.DataFrame] = None,
             col: Optional[str] = None,
             pivot_kwarg: Optional[Dict[str, Any]] = None,
             heatmap_kwarg: Optional[Dict[str, Any]] = None,
             cbar_kws: Optional[Dict[str, Any]] = None) -> mplt.axes.Axes:
    """heatplot.

    Parameters
    ----------
    data : Optional[pd.DataFrame]
        data
    col : Optional[str]
        col
    pivot_kwarg : Optional[Dict[str, Any]]
        pivot_kwarg
    heatmap_kwarg : Optional[Dict[str, Any]]
        heatmap_kwarg
    cbar_kws : Optional[Dict[str, Any]]
        cbar_kws
    kwargs :
        kwargs

    Returns
    -------
    mplt.axes.Axes

    """
    cbar_kws = {'label': 'Action P'} if cbar_kws is None else cbar_kws
    assert col is not None

    f_grid = sns.FacetGrid(data, col=col)
    cbar_ax = f_grid.fig.add_axes([1.0, .15, .03, .7])
    f_grid.map_dataframe(draw_heatmap, pvt_kwarg=pivot_kwarg,
                          htm_kwarg=heatmap_kwarg, cbar_ax=cbar_ax,
                          cbar_kws=cbar_kws)
    return f_grid

@plot
def heatmap(*args, data: pd.DataFrame = None, **kwargs) -> mplt.axes.Axes:
    """heatmap.

    Parameters
    ----------
    args :
        args
    data : pd.DataFrame
        data
    kwargs :
        kwargs

    Returns
    -------
    mplt.axes.Axes

    """
    return sns.heatmap(data=data, *args, **kwargs)
