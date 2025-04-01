# © 2025 Nokia
# Licensed under the BSD 3-Clause License
# SPDX-License-Identifier: BSD-3-Clause
#
# Contact: Mattia Milani (Nokia) <mattia.milani@nokia.com>

from typing import Optional
import datetime
import pandas as pd
import seaborn as sns
import matplotlib as mplt

from darf.src.decorators.decorators import plot

@plot
def line_double_y_axis(*args, data: pd.DataFrame = None,
                       yaxis_1_kwargs: Optional[dict] = None,
                       yaxis_2_kwargs: Optional[dict] = None,
                       **kwargs) -> mplt.axes.Axes:
    """line_double_y_axis.

    Apply a line plot with double y axis

    Both kwargs must be provided otherwise an expection is raised

    Parameters
    ----------
    data : pd.DataFrame
        The input data
    yaxis_1_kwargs : dict
        The first y axis kwargs
    yaxis_2_kwargs : dict
        The second y axis kwargs
    kwargs :
        kwargs

    Returns
    -------
    mplt.axes.Axes
        Current axes

    Raises
    ------
    ValueError
        If one of the yaxis kwargs is missing
    """
    if yaxis_1_kwargs is None or yaxis_2_kwargs is None:
        raise ValueError("Both yaxis kwargs must be provided")

    fig, ax1 = mplt.pyplot.subplots()
    ax2 = ax1.twinx()


    # Check if a palette is present in the kwargs
    if 'palette' in kwargs:
        palette = kwargs.pop('palette')

    if 'palette' not in yaxis_1_kwargs:
        yaxis_1_kwargs['palette'] = palette
    if 'palette' not in yaxis_2_kwargs:
        yaxis_2_kwargs['palette'] = palette

    sns.lineplot(data=data, **yaxis_1_kwargs, **kwargs, ax=ax1)
    sns.lineplot(data=data, **yaxis_2_kwargs, **kwargs, ax=ax2)

    return ax1
