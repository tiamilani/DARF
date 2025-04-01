# © 2025 Nokia
# Licensed under the BSD 3-Clause License
# SPDX-License-Identifier: BSD-3-Clause
#
# Contact: Mattia Milani (Nokia) <mattia.milani@nokia.com>

"""
Module plot_functions
=====================

This module contains all the function to generate a plot
"""

from typing import Any, Dict, Optional, Callable, List
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib as mplt
from sklearn.preprocessing import normalize as norm
from statsmodels.graphics.tsaplots import plot_acf
from darf.src.decorators.decorators import plot

@plot
def multi_dim_evolution(*args,
                      data: Optional[pd.DataFrame] = None,
                      facet_kwargs: Optional[Dict[str, Any]] = None,
                      map_fct: Optional[Callable] = None,
                      **kwargs) -> mplt.axes.Axes:
    """multiDimEvolution.

    Parameters
    ----------
    args :
        args
    data : Optional[pd.DataFrame]
        data
    facet_kwargs : Optional[Dict[str, Any]]
        facet_kwargs
    map_fct : Optional[Callable]
        map_fct
    kwargs :
        kwargs

    Returns
    -------
    mplt.axes.Axes

    """
    if data is None:
        raise ValueError("The dataframe cannot be None")
    default_facet_kw = {}
    if facet_kwargs is not None:
        default_facet_kw.update(facet_kwargs)

    map_fct = sns.kdeplot if map_fct is None else map_fct
    f_grid = sns.FacetGrid(data, **default_facet_kw)
    f_grid.map(map_fct, *args, **kwargs)
    return f_grid

@plot
def multi_line(key_col: str, *args,
                  data: Optional[pd.DataFrame] = None,
                  **kwargs) -> mplt.axes.Axes:
    """multiLineplot.

    Parameters
    ----------
    key_col : str
        key_col
    args :
        args
    data : Optional[pd.DataFrame]
        data
    kwargs :
        kwargs

    Returns
    -------
    mplt.axes.Axes

    """
    if data is None:
        raise ValueError("The dataframe cannot be None")

    objs = data[key_col].unique()
    ax = None
    for c in objs:
        sub_df = data[data[key_col] == c]
        if ax is None:
            ax = sns.lineplot(sub_df, *args, **kwargs)
        else:
            ax = sns.lineplot(sub_df, *args, ax=ax, **kwargs)
        ax.fill_between(sub_df["Step"], sub_df["Value"], 0.0, alpha=1)
    return ax
