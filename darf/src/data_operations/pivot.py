# © 2025 Nokia
# Licensed under the BSD 3-Clause License
# SPDX-License-Identifier: BSD-3-Clause
#
# Contact: Mattia Milani (Nokia) <mattia.milani@nokia.com>

"""
pivot Module
============

Contains operations relatives to the pivot of dataframes
"""

from typing import List, Optional

import numpy as np
import pandas as pd

from darf.src.decorators import data_op

@data_op
def pivot(df: pd.DataFrame,
          id_vars: Optional[List[str]] = None,
          columns: Optional[List[str]] = None,
          hue_clm: str = "Statistics",
          val_clm: str = "Value") -> pd.DataFrame:
    """pivot.
    Pivot a dataframe using df.melt

    Parameters
    ----------
    df : pd.DataFrame
        df
    id_vars : List[str]
        id_vars
    columns : List[str]
        columns
    hue_clm : str
        hue_clm
    val_clm : str
        val_clm

    Returns
    -------
    pd.DataFrame

    """
    id_vars = id_vars if not id_vars is None else ["exp_id", "epoch"]
    columns = columns if not columns is None else ["distance_accuracy","loss"]
    return df.melt(id_vars=id_vars,
                   value_vars=columns,
                   var_name=hue_clm,
                   value_name=val_clm)

# pylint: disable=too-many-arguments
@data_op
def train_val_pivot(df: pd.DataFrame,
                    clm_keywords: Optional[List[str]] = None,
                    val_prefix: str = "val_",
                    hue_clm: str = "Statistics",
                    hue_id: Optional[List[str]] = None,
                    val_clm: str = "Value",
                    val_id: Optional[List[str]] = None,
                    join_cols: Optional[List[str]] = None,
                    remove_inner_duplicates: bool = True) -> pd.DataFrame:
    """train_val_pivot.
    Pivot the data to have the training and validation statistics in the same row.

    Parameters
    ----------
    df : pd.DataFrame
        The input data
    clm_keywords : List[str]
        List of column keywords
    val_prefix : str
        Prefix for the validation columns, will be applied to the clm_keyword
        to get the validation columns
    hue_clm : str
        The column name for the hue
    hue_id : List[str]
        List of hue ids for multiple statistics that should be separated
    val_clm : str
        The column name for the value
    val_id : List[str]
        List of value ids for multiple statistics that should be separated
    join_cols : List[str]
        List of columns that should be used to join the data
    remove_inner_duplicates : bool
        Flag to remove the inner duplicates, default is True
    args : List
        List of arguments

    Returns
    -------
    pd.DataFrame
        The pivoted data
    """
    clm_keywords = clm_keywords if not clm_keywords is None else ["distance_accuracy", "loss"]
    hue_id = hue_id if not hue_id is None else ["accuracy", "loss"]
    val_id = val_id if not val_id is None else ["accuracy", "loss"]
    join_cols = join_cols if not join_cols is None else ["exp_id", "epoch"]
    assert len(clm_keywords) == len(hue_id) == len(val_id)

    dfs = []
    for clm, hue, val in zip(clm_keywords, hue_id, val_id):
        tmp_df = df.melt(id_vars=join_cols,
                        value_vars=[clm, val_prefix+clm],
                        var_name=hue_clm+"_"+hue,
                        value_name=val_clm+"_"+val)
        dfs.append(tmp_df)

    merged = pd.merge(dfs[0], dfs[1], how="inner", on=join_cols)
    if remove_inner_duplicates:
        keep = np.array([True, False, False, True])
        num_epochs = int(len(merged)/4)
        keep = np.tile(keep, num_epochs)
        merged = merged[keep]
    return merged

@data_op
def df_pivot(df: pd.DataFrame, *args,
             **kwargs) -> pd.DataFrame:
    """df_pivot.
    wraper arround pandas meld function

    Parameters
    ----------
    df : pd.DataFrame
        The input data
    args : List
        List of arguments
    kwargs : Dict
        Dictionary of keyword arguments

    Returns
    -------
    pd.DataFrame
        The pivoted data
    """

    tmp_df = df.melt(*args, **kwargs)
    return tmp_df
