# © 2025 Nokia
# Licensed under the BSD 3-Clause License
# SPDX-License-Identifier: BSD-3-Clause
#
# Contact: Mattia Milani (Nokia) <mattia.milani@nokia.com>

"""
drop Module
===========

Contains operations relatives to the rename of dataframes
"""

from typing import List, Any, Dict, Optional

import numpy as np
import pandas as pd

from itertools import groupby
from operator import itemgetter
from darf.src.io import Pb as pb

from darf.src.decorators import data_op

@data_op
def drop_row(df: pd.DataFrame,
             clm: str = "",
             val: str = "",
             keep_head: int = 0,
             keep_tail: int = 0) -> pd.DataFrame:
    """drop_rows.
    Drop rows based on a column value.
    If the input is empty then the DF is returned as is.

    Parameters
    ----------
    df : pd.DataFrame
        The input data
    clm : str
        The column to check
    val : str
        The value to check
    keep_head: int
        Number of rows that should be kept at the beginning of each
        drop section identified
    keep_tail: int
        Number of rows that should be kept at the end of each dropped section

    Returns
    -------
    pd.DataFrame
        The DataFrame with the rows dropped
    """
    if clm and val and (keep_head == 0 and keep_tail == 0):
        return df[df[clm] != val]

    # Identify all the sections that should be dropped
    drop_sections = df[df[clm] == val].index
    start = []
    end = []
    for k, g in groupby(enumerate(drop_sections), lambda ix: ix[0] - ix[1]):
        elems = list(map(itemgetter(1), g))
        start.append(elems[0])
        end.append(elems[-1])

    start = np.array(start)
    end = np.array(end)
    groups = np.stack([start, end], axis=1)

    start += keep_head
    end -= keep_tail
    diff = end - start
    groups = groups[diff >= 0]
    drop_indexes = np.concatenate([np.arange(start[i], end[i]+1) for i in range(len(groups))])
    tmp_df = df.drop(drop_indexes)

    # for group in groups:
    #     start = group[0] + keep_head
    #     end = group[1] - keep_tail
    #     if end < start:
    #         continue
    #     df = df.drop(df.index[start:end+1])

    return tmp_df

@data_op
def drop_clm(df: pd.DataFrame, *args,
             clm: Optional[List[str]] = None,
             apply_intersection: bool = False,
             **kwargs) -> pd.DataFrame:
    """drop_clm.
    Drop columns from the DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        The input data
    args : List
        List of arguments
    clm : List[str]
        List of columns to drop
    apply_intersection : bool
        Flag to apply the intersection of the columns to drop with the current
        columns of the dataset.
    kwargs : Dict
        Dictionary of keyword arguments

    Returns
    -------
    pd.DataFrame
        The DataFrame with the columns dropped
    """
    clm = clm if clm is not None else []
    if apply_intersection:
        clm = list(set(clm) & set(df.columns))
    return df.drop(*args, columns=clm, axis=0, **kwargs)

@data_op
def drop_nan(df: pd.DataFrame) -> pd.DataFrame:
    """drop_nan.
    Drop the rows with NaN values.

    Parameters
    ----------
    df : pd.DataFrame
        The input data

    Returns
    -------
    pd.DataFrame
        The DataFrame without the NaN values
    """
    return df.dropna()

@data_op
def drop_anomaly(df: pd.DataFrame,
                 id_clm: str = "exp_id",
                 anomaly_clm: str = "anomaly",
                 anomalies: Optional[Dict[str, Any]] = None,
                 remove_all: bool = True) -> pd.DataFrame:
    """drop_anomaly.
    Drop the anomalies from the DataFrame.
    Anomalies are defined in a dictionary, where the key define the function
    that would be applied with a match case and the item are the arguments
    for the function.

    Parameters
    ----------
    df : pd.DataFrame
        The input data
    id_clm : str
        The column that defines the id, when an anomaly is found if the
        remove_all flag is active this will be used to remove the entire object
        identified by the id.
    anomaly_clm : str
        The column where to look for the anomaly
    anomalies : Dict[str, Any]
        Dictionary of anomalies to look for, the key identifies the function to
        call and the item the arguments for the function
    remove_all : bool
        Flag to remove the entire object identified by the id_clm if an anomaly
        is found

    Returns
    -------
    pd.DataFrame
        The DataFrame without the anomalies
    """
    anomalies = anomalies if anomalies is not None else {}

    def drop_nan(df: pd.DataFrame, anomaly_clm: str) -> pd.DataFrame:
        if remove_all:
            # Get the id of the object to remove
            ids = df[df[anomaly_clm].isna()][id_clm].unique()
            # Drop all the elemets with that id
            return df[~df[id_clm].isin(ids)]
        return df.dropna(subset=[anomaly_clm])

    def drop_lw_eq(df: pd.DataFrame, anomaly_clm: str, value: float) -> pd.DataFrame:
        if remove_all:
            # Get the id of the object to remove
            ids = df[df[anomaly_clm] <= value][id_clm].unique()
            # Drop all the elemets with that id
            return df[~df[id_clm].isin(ids)]
        return df[df[anomaly_clm] > value]

    def drop_group_sum(df: pd.DataFrame, anomaly_clm: str, group_clm: str,
                       group_value: str, value: float) -> pd.DataFrame:
        if remove_all:
            # Get the id of the object to remove
            ids = df.groupby([group_clm, id_clm]).sum().reset_index()
            ids_grp_val = ids[group_clm] == group_value
            ids_anomaly = ids[anomaly_clm] <= float(value)
            ids = ids[(ids_grp_val) & (ids_anomaly)][id_clm].unique()
            # Drop all the elemets with that id
            return df[~df[id_clm].isin(ids)]
        raise NotImplementedError("drop_group_sum without remove_all not implemented yet")

    tmp_df = df.copy()
    for anomaly, args in anomalies.items():
        match anomaly:
            case 'NaN':
                tmp_df = drop_nan(tmp_df, anomaly_clm)
            case 'LwEq':
                tmp_df = drop_lw_eq(tmp_df, anomaly_clm, *args)
            case 'GroupSum':
                tmp_df = drop_group_sum(tmp_df, anomaly_clm, *args)
            case _:
                raise ValueError(f"Anomaly function {anomaly} not recognized")
    return tmp_df

@data_op
def keep_only(df: pd.DataFrame,
              id_clm: str = "exp_id",
              keep: Optional[List[str]] = None) -> pd.DataFrame:
    """keep_only.

    Keep only the elments in 'id_clm' that have a value in 'keep'.

    Parameters
    ----------
    df : pd.DataFrame
        The input data
    id_clm : str
        The column to check
    keep : List[str]
        List of values to keep

    Returns
    -------
    pd.DataFrame
        The DataFrame with only the elements to keep
    """
    keep = keep if keep is not None else []
    return df[df[id_clm].isin(keep)]

@data_op
def drop_windows(df: pd.DataFrame,
                 id_clm: str = "op_id",
                 window_size: int = 120,
                 stride: int = 1) -> pd.DataFrame:
    """drop_windows.

    Given a time series dataset a lot of time data is treated as windows.
    But when you have multiple 'index_ids' in your dataset you may don't
    want to have mixed windows.
    A window that starts with idx_id=0 and terminates in idx_id=1 most of
    time is a programming error and might lead to errors.

    This function is meant to drop the elements that would be in a mixed window.

    Parameters
    ----------
    df : pd.DataFrame
        df
    window_size : int
        window_size
    stride : int
        stride

    Returns
    -------
    pd.DataFrame

    """
    duration = df.groupby(id_clm).count().values[0][0]
    n_true = int((duration-(window_size-1))/stride)
    n_false = int((window_size-1)/stride)
    mask = np.array([[False]*n_false + [True]*n_true])
    mask = np.repeat(mask, len(df)/duration, axis=0).flatten()
    # mask_idx = np.where(mask)[0]
    # print(mask_idx)
    # print(len(mask_idx))
    return df[mask]

@data_op
def drop_consecutive_timestamps(df: pd.DataFrame,
                                id_clm: str = "timestamp",
                                delta: int = 1) -> pd.DataFrame:
    """drop_consecuttive_timestamps.

    Function to drop consecutive alerts for the same anomaly.
    If the folowing alert is within delta secodns from the previous
    one then it is dropped.

    Parameters
    ----------
    df : pd.DataFrame
        df
    id_clm : str
        id_clm
    delta : int
        delta

    Returns
    -------
    pd.DataFrame

    """
    df[id_clm] = pd.to_datetime(df[id_clm])
    diff = df[id_clm].diff()
    mask = diff.dt.total_seconds() > delta
    df = df[mask]
    return df

@data_op
def drop_lt(df: pd.DataFrame,
            clm: str,
            value: float) -> pd.DataFrame:
    """drop_lt.

    Drop the rows where the value in 'clm' is less than 'value'.

    Parameters
    ----------
    df : pd.DataFrame
        The input data
    clm : str
        The column to check
    value : float
        The value to check

    Returns
    -------
    pd.DataFrame
        The DataFrame with the rows dropped
    """
    return df[df[clm] >= value]

@data_op
def keep_lowest(df: pd.DataFrame,
                clm: str,
                n: int) -> pd.DataFrame:
    """keep_lowest

    Keep the n lowest values in 'clm'.

    Parameters
    ----------
    df : pd.DataFrame
        The input data
    clm : str
        The column to check
    n : int
        The number of lowest values to keep

    Returns
    -------
    pd.DataFrame
        The DataFrame with only the n lowest values
    """
    return df.nsmallest(n, clm)

@data_op
def keep_egt(df: pd.DataFrame,
             id_clm: str = "id",
             value: float = None) -> pd.DataFrame:
    """keep_egt.

    Keep only rows which have the value in 'id_clm' equal or grather than
    'value'.

    Parameters
    ----------
    df : pd.DataFrame
        The input data
    id_clm : str
        The column to check
    value : float
        The value to check

    Returns
    -------
    pd.DataFrame
        The DataFrame with only the rows that satisfy the condition

    Raises
    ------
    ValueError
        If the value is not provided
    """
    if value is None:
        raise ValueError("Value to check not provided")

    return df[df[id_clm] >= value]

@data_op
def keep_elt(df: pd.DataFrame,
             id_clm: str = "id",
             value: Any = None) -> pd.DataFrame:
    """keep_elt.

    Keep only the rows where the value in 'clm' is equal or lower than 'value'.

    Parameters
    ----------
    df : pd.DataFrame
        The input data
    clm : str
        The column to check
    value : Any
        The value to check

    Returns
    -------
    pd.DataFrame
        The DataFrame with only the rows that satisfy the condition

    Raises
    ------
    ValueError
        if the value is not provided
    """
    if value is None:
        raise ValueError("Value to check not provided")
    return df[df[id_clm] <= value]
