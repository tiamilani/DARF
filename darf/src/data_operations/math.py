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

from typing import List, Optional
import numpy as np
import pandas as pd

from darf.src.decorators import data_op

@data_op
def add_columns(df: pd.DataFrame,
                columns: Optional[List[str]] = None,
                value: float = 0.0) -> pd.DataFrame:
    """add_columns.

    Add the values to the columns.

    Parameters
    ----------
    df : pd.DataFrame
        The input data
    columns : Optional[List[str]]
        The columns to sum, default None
    value: float
        The value to add to the columns

    Returns
    -------
    pd.DataFrame
        The DataFrame with the new column
    """
    columns = [] if columns is None else columns
    df[columns] = df[columns] + value
    return df

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
                columns: Optional[List[str]] = None,
                new_clm: str = "sum") -> pd.DataFrame:
    """sum_columns.

    Sum the values of the columns and put the result in a new column.

    Parameters
    ----------
    df : pd.DataFrame
        The input data
    columns : Optional[List[str]]
        The columns to sum, default None
    new_clm : str
        The name of the new column

    Returns
    -------
    pd.DataFrame
        The DataFrame with the new column
    """
    columns = [] if columns is None else columns
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

@data_op
def apply_sigmoid(df: pd.DataFrame,
                  clm: str = "",
                  c: float = 1.0,
                  k: float = 1.0,
                  m: float = 0.0,
                  n: float = 0.0) -> pd.DataFrame:
    """apply_sigmoid.
    Apply the sigmoid function to a column.
    The sigmoid function is defined as:
    f(x) = c * (1 / (1 + e^(-(k * x) + m)))) + n
    where:
    - c is the amplitude
    - k is the steepness of the curve
    - m is the x-value of the sigmoid's midpoint
    - n is the y-value of the sigmoid's midpoint

    Parameters
    ----------
    df : pd.DataFrame
        The input data
    clm : str
        The column to apply the sigmoid function
    c : float
        The amplitude of the sigmoid function
    k : float
        The steepness of the curve
    m : float
        The x-value of the sigmoid's midpoint
    n : float
        The y-value of the sigmoid's midpoint

    Returns
    -------
    pd.DataFrame
        The DataFrame with the new column

    Raises
    ------
    ValueError
        If the column is not in the DataFrame
    """
    if clm not in df.columns:
        raise ValueError(f"Column {clm} not in DataFrame")
    tmp_df = df.copy()
    tmp_df[clm] = c * (1 / (1 + np.exp(-(k * tmp_df[clm]) + m))) + n
    return tmp_df

@data_op
def transform_sigmoid(df: pd.DataFrame,
                  clm: str = "",
                  val: str = "",
                  c: float = 1.0,
                  k: float = 1.0,
                  m: float = 0.0,
                  n: float = 0.0) -> pd.DataFrame:
    """apply_sigmoid.
    Apply the sigmoid function to a column.
    The sigmoid function is defined as:
    f(x) = c * (1 / (1 + e^(-(k * x) + m)))) + n
    where:
    - c is the amplitude
    - k is the steepness of the curve
    - m is the x-value of the sigmoid's midpoint
    - n is the y-value of the sigmoid's midpoint

    Parameters
    ----------
    df : pd.DataFrame
        The input data
    clm : str
        The column to apply the sigmoid function
    c : float
        The amplitude of the sigmoid function
    k : float
        The steepness of the curve
    m : float
        The x-value of the sigmoid's midpoint
    n : float
        The y-value of the sigmoid's midpoint

    Returns
    -------
    pd.DataFrame
        The DataFrame with the new column

    Raises
    ------
    ValueError
        If the column is not in the DataFrame
    """
    if clm not in df.columns:
        raise ValueError(f"Column {clm} not in DataFrame")
    tmp_df = df.copy()
    tmp_df.reset_index(drop=True, inplace=True)
    for row in tmp_df.iterrows():
        index = row[0]
        stat = row[1][clm]
        h_val = row[1]['Value']
        if stat == val:
            tmp_df.at[index, 'Value'] = c * (1 / (1 + np.exp(-(k * h_val) + m))) + n
    return tmp_df

@data_op
def compute_ratio(df: pd.DataFrame,
                  clm_a: str = "",
                  clm_b: str = "",
                  new_clm: str = "ratio") -> pd.DataFrame:
    """compute_ratio.
    Compute the ratio between two columns.

    The two columns must exist in the DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        The input data
    clm_a : str
        The first column to compute the ratio
    clm_b : str
        The second column to compute the ratio
    new_clm : str
        The name of the new column

    Returns
    -------
    pd.DataFrame
        The DataFrame with the new column

    Raises
    ------
    ValueError
        If the columns are not in the DataFrame
    """
    if clm_a not in df.columns:
        raise ValueError(f"Column {clm_a} not in DataFrame")
    if clm_b not in df.columns:
        raise ValueError(f"Column {clm_b} not in DataFrame")

    df[new_clm] = df[clm_a] / df[clm_b]
    return df
