# © 2025 Nokia
# Licensed under the BSD 3-Clause License
# SPDX-License-Identifier: BSD-3-Clause
#
# Contact: Mattia Milani (Nokia) <mattia.milani@nokia.com>

"""
Rolling Module
===========

apply rolling operations to the dataframe
"""

from typing import List
import numpy as np
import pandas as pd

from darf.src.decorators import data_op

@data_op
def rolling_ratio(df: pd.DataFrame,
                  clm_a: str = "",
                  clm_b: str = "",
                  window: int = 1,
                  new_clm: str = "ratio",
                  **kwargs) -> pd.DataFrame:
    """rolling_ratio.

    Calculate the rolling ratio of two columns.
    For each row the rolling sum of the column `clm_a` is divided by the rolling sum of the column `clm_b`
    with a window in the past up to `window` rows.

    All kwargs are passed to the pandas rolling function.
    reference: [df.rolling](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.rolling.html)

    Parameters
    ----------
    df : pd.DataFrame
        The input data
    clm_a : str
        The first column to calculate the rolling ratio
    clm_b : str
        The second column to calculate the rolling ratio
    window : int
        The window size to calculate the rolling ratio
    new_clm : str
        The name of the new column to store the rolling ratio
    **kwargs : dict
        Additional arguments to pass to the pandas rolling function

    Returns
    -------
    pd.DataFrame
        The input data with the new column `new_clm` containing the rolling ratio

    Raises
    -------
    ValueError
        If the columns `clm_a` or `clm_b` are not present in the dataframe
    """

    if clm_a not in df.columns:
        raise ValueError(f"Column {clm_a} not found in the dataframe")
    if clm_b not in df.columns:
        raise ValueError(f"Column {clm_b} not found in the dataframe")

    sum_a = df[clm_a].rolling(window=window, **kwargs).sum()
    sum_b = df[clm_b].rolling(window=window, **kwargs).sum()
    df[new_clm] = sum_a / (sum_a + sum_b)

    return df