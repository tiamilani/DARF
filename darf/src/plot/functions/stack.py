# © 2025 Nokia
# Licensed under the BSD 3-Clause License
# SPDX-License-Identifier: BSD-3-Clause
#
# Contact: Mattia Milani (Nokia) <mattia.milani@nokia.com>

"""
Stack plot functions module
===========================

Module which contains functions built on top of stackplots
"""

from typing import Optional
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib as mplt
from sklearn.preprocessing import normalize as norm
from statsmodels.graphics.tsaplots import plot_acf
from darf.src.decorators.decorators import plot

@plot
def line_stack(*args,
              data: Optional[pd.DataFrame] = None,
              x: Optional[str] = None,
              y: Optional[str] = None,
              hue: Optional[str] = None,
              normalize: bool = False,
              **kwargs) -> mplt.axes.Axes:
    """lineStack.

    Parameters
    ----------
    args :
        args
    data : Optional[pd.DataFrame]
        data
    x : Optional[str]
        x
    y : Optional[str]
        y
    hue : Optional[str]
        hue
    normalize : bool
        normalize
    kwargs :
        kwargs

    Returns
    -------
    mplt.axes.Axes

    """
    if data is None:
        raise ValueError("The dataframe for a lineStack cannot be None")

    x = data[x].unique()
    a = np.stack([data[data[hue] == h][y].values for h in data[hue].unique()], axis=-1)
    if normalize:
        a = norm(a, axis=1, norm='l1')
    a = np.around(a, 3)
    a = np.transpose(a)
    y_plt = {
            h: a[i] for i, h in enumerate(data[hue].unique())
        }
    _, ax = mplt.pyplot.subplots()
    ax.stackplot(x, y_plt.values(), *args, labels=y_plt.keys(), **kwargs)
    ax.legend(loc='upper left')
    return ax

