# © 2025 Nokia
# Licensed under the BSD 3-Clause License
# SPDX-License-Identifier: BSD-3-Clause
#
# Contact: Mattia Milani (Nokia) <mattia.milani@nokia.com>

"""
math Module
===========

Contains operations relatives to math operations on dataframes
"""

from typing import List
import numpy as np
import pandas as pd

from darf.src.decorators import data_op

@data_op
def multiply_column(df: pd.DataFrame,
                     clm: str = "",
                     x: float = 1.0) -> pd.DataFrame:
    """multiply_column.
    Multiply the values of a column by a factor.

    Parameters
    ----------
    df : pd.DataFrame
        The input data
    clm : str
        The column to multiply
    x : float
        The factor to multiply

    Returns
    -------
    pd.DataFrame
        The DataFrame with the multiplied column
    """
    df[clm] = df[clm]*x
    return df

@data_op
def sum_columns(df: pd.DataFrame,
                columns: List[str] = [],
                new_clm: str = "sum") -> pd.DataFrame:
    """sum_columns.

    Sum the values of the columns and put the result in a new column.

    Parameters
    ----------
    df : pd.DataFrame
        The input data
    columns : List[str]
        The columns to sum
    new_clm : str
        The name of the new column

    Returns
    -------
    pd.DataFrame
        The DataFrame with the new column
    """
    df[new_clm] = df[columns].sum(axis=1)
    return df

@data_op
def window_mean_ratio(df: pd.DataFrame,
                      mean_clm: str = "mean",
                      window: int = 1,
                      new_clm: str = "ratio",
                      group_by: str = "op_id") -> pd.DataFrame:
    """window_mean_ratio.

    Apply the ratio between the current value of `mean_clm` and the mean of
    the past window values.
    This is used to identify the variation in comparisong to a moving average.
    Is possible to apply the operation to groups of data.

    Parameters
    ----------
    df : pd.DataFrame
        The input data
    mean_clm : str
        The column to calculate the ratio
    window : int
        The window size
    new_clm : str
        The name of the new column
    group_by : str
        The column to group the data

    Returns
    -------
    pd.DataFrame
        The DataFrame with the new column
    """
    # mean  = df[mean_clm].values[:1000]
    # mean = np.mean(mean)
    # print(mean)
    # df[new_clm] = df.groupby(group_by)[mean_clm].transform(lambda x: x[:1000].mean())
    # df[new_clm] = df[mean_clm]/df[new_clm]

    df[new_clm] = df.groupby(group_by)[mean_clm].transform(lambda x: x.rolling(window).mean())
    df[new_clm] = df[mean_clm]/df[new_clm]
    # print(mean)
    # raise Exception
    return df
