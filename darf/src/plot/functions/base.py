# © 2025 Nokia
# Licensed under the BSD 3-Clause License
# SPDX-License-Identifier: BSD-3-Clause
#
# Contact: Mattia Milani (Nokia) <mattia.milani@nokia.com>

"""
Base plot functions module
==========================

This module contains the basic plot functions that can be used to create a figure.
Mostly all the functions are wrappers around seaborn or matplotlib functions.
"""
from typing import Optional
import pandas as pd
import seaborn as sns
import matplotlib as mplt
from statsmodels.graphics.tsaplots import plot_acf
from darf.src.decorators.decorators import plot

@plot
def kde(*args, data: pd.DataFrame = None, **kwargs) -> None:
    """kde.
    Plot a KDE plot

    Parameters
    ----------
    args :
        args to pass to sns.kdeplot
    data : pd.DataFrame
        dataset used for the kde plot
    kwargs :
        kwargs for the kde plot

    Returns
    -------
    None

    """
    return sns.kdeplot(data=data, *args, **kwargs)

@plot
def joint(*args, data: pd.DataFrame = None, **kwargs) -> None:
    """joint.
    use sns.jointplot

    Parameters
    ----------
    args :
        args to pass to sns.jointplot
    data : pd.DataFrame
        data to use for the jointplot
    kwargs :
        kwargs for the jointplot

    Returns
    -------
    None

    """
    return sns.jointplot(data=data, *args, **kwargs)

@plot
def ecdf(*args, data: pd.DataFrame = None, **kwargs) -> None:
    """ecdf.

    Parameters
    ----------
    args :
        args to pass to sns.ecdfplot
    data : pd.DataFrame
        data to use for the ecdfplot
    kwargs :
        kwargs for the ecdfplot

    Returns
    -------
    None

    """
    return sns.ecdfplot(data=data, *args, **kwargs)

@plot
def displot(*args, data: pd.DataFrame = None, **kwargs) -> mplt.axes.Axes:
    """displot.
    sns.displot wrapper

    Parameters
    ----------
    args :
        args to pass to sns.displot
    data : pd.DataFrame
        data to use for the displot
    kwargs :
        kwargs for the displot

    Returns
    -------
    mplt.axes.Axes

    """
    return sns.displot(data=data, *args, **kwargs)

@plot
def scatter(*args, data: pd.DataFrame = None, **kwargs) -> None:
    """scatter.

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
    None

    """
    return sns.scatterplot(data=data, *args, **kwargs)

@plot
def line(*args, data: pd.DataFrame = None, **kwargs) -> mplt.axes.Axes:
    """line.

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
    return sns.lineplot(data=data, *args, **kwargs)

@plot
def violin(*args, data: pd.DataFrame = None, **kwargs) -> mplt.axes.Axes:
    """violin.

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
    return sns.violinplot(data=data, *args, **kwargs)

@plot
def boxplot(*args, data: pd.DataFrame = None, **kwargs) -> mplt.axes.Axes:
    """boxplot.

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
    return sns.boxplot(data=data, *args, **kwargs)

@plot
def distplot(*args, data: pd.DataFrame = None, **kwargs) -> mplt.axes.Axes:
    """distplot.

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
    return sns.boxplot(data=data, *args, **kwargs)

@plot
def cat(*args, data: Optional[pd.DataFrame] = None, **kwargs) -> None:
    """cat.

    Parameters
    ----------
    args :
        args
    data : Optional[pd.DataFrame]
        data
    kwargs :
        kwargs

    Returns
    -------
    None

    """
    if data is None:
        raise ValueError("The dataframe for a catplot cannot be None")
    return sns.catplot(data=data, *args, **kwargs)

@plot
def histplot(*args, data: Optional[pd.DataFrame] = None, **kwargs) -> None:
    """histplot.

    Parameters
    ----------
    args :
        args
    data : Optional[pd.DataFrame]
        data
    kwargs :
        kwargs

    Returns
    -------
    None

    """
    if data is None:
        raise ValueError("The dataframe for a catplot cannot be None")
    return sns.histplot(data=data, *args, **kwargs)

@plot
def acf(data: Optional[pd.DataFrame] = None, column: Optional[str] = None):
    """acf.

    Parameters
    ----------
    data : Optional[pd.DataFrame]
        data
    column : Optional[str]
        column
    """
    if column is None:
        raise ValueError("A column must be specified")
    return plot_acf(data[column].values)

@plot
def barplot(*args, data: Optional[pd.DataFrame] = None, **kwargs):
    """barplot.

    Parameters
    ----------
    args :
        args
    data : Optional[pd.DataFrame]
        data
    kwargs :
        kwargs
    """
    if data is None:
        raise ValueError("The dataframe cannot be None")
    return sns.barplot(data=data, *args, **kwargs)

@plot
def relplot(*args, data: Optional[pd.DataFrame] = None, **kwargs):
    """relplot.

    Parameters
    ----------
    args :
        args
    data : Optional[pd.DataFrame]
        data
    kwargs :
        kwargs
    """
    if data is None:
        raise ValueError("The dataframe cannot be None")

    return sns.relplot(data=data, *args, **kwargs)

@plot
def pairgrid(*args, data: Optional[pd.DataFrame] = None,
             lower: Optional[str] = None,
             diag: Optional[str] = None,
             upper: Optional[str] = None,
             **kwargs):
    """pairgrid.

    Parameters
    ----------
    args :
        args
    data : Optional[pd.DataFrame]
        data
    kwargs :
        kwargs
    """
    if data is None:
        raise ValueError("The dataframe cannot be None")
    p = sns.PairGrid(data=data, *args, **kwargs)

    if lower is not None:
        match lower:
            case 'scatter':
                p.map_lower(sns.scatterplot)
            case 'kde':
                p.map_lower(sns.kdeplot)
            case 'hist':
                p.map_lower(sns.histplot)
            case _:
                raise ValueError("Invalid lower value")

    if diag is not None:
        match diag:
            case 'kde':
                p.map_diag(sns.kdeplot)
            case 'hist':
                p.map_diag(sns.histplot)
            case _:
                raise ValueError("Invalid diag value")

    if upper is not None:
        match upper:
            case 'scatter':
                p.map_upper(sns.scatterplot)
            case 'kde':
                p.map_upper(sns.kdeplot)
            case 'hist':
                p.map_upper(sns.histplot)
            case _:
                raise ValueError("Invalid upper value")

    return p


