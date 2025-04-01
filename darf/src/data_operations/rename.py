# © 2025 Nokia
# Licensed under the BSD 3-Clause License
# SPDX-License-Identifier: BSD-3-Clause
#
# Contact: Mattia Milani (Nokia) <mattia.milani@nokia.com>

"""
rename Module
=============

Contains operations relatives to the rename of dataframes
"""

from typing import List, Optional, Any

import pandas as pd

from darf.src.decorators import data_op

@data_op
def rename_clm(df: pd.DataFrame,
                old_clm: Optional[List[str]] = None,
                new_clm: Optional[List[str]] = None,
                **kwargs) -> pd.DataFrame:
    """rename.
    Rename the columns of the dataframe.

    Parameters
    ----------
    df : pd.DataFrame
        The input data
    old_clm : List[str]
        List of old column names
    new_clm : List[str]
        List of new column names
    kwargs : Dict
        Dictionary of keyword arguments

    Returns
    -------
    pd.DataFrame
        The renamed DataFrame
    """
    old_clm = old_clm if not old_clm is None else []
    new_clm = new_clm if not new_clm is None else []

    assert len(old_clm) == len(new_clm)
    rename_dict = dict(zip(old_clm, new_clm))
    df.rename(columns=rename_dict, inplace=True, **kwargs)
    return df

@data_op
def rename_val(df: pd.DataFrame,
               old_val: Optional[List[str]] = None,
               new_val: Optional[List[str]] = None,
               **kwargs) -> pd.DataFrame:
    """rename_val.
    Rename the values of the dataframe.
    It uses the pandas ``cat.rename_categoris`` method for categorical columns
    and ``replace`` method for the other columns.

    Parameters
    ----------
    df : pd.DataFrame
        The input data
    old_val : List[str]
        List of old values
    new_val : List[str]
        List of new values
    kwargs : Dict
        Dictionary of keyword arguments

    Returns
    -------
    pd.DataFrame
        The renamed DataFrame
    """
    old_val = old_val if not old_val is None else []
    new_val = new_val if not new_val is None else []

    tmp_df = df.copy()
    # For all the categorical column in the dataframe use the series method
    # ``cat.rename_categories`` to rename the categories
    cat_cols = tmp_df.select_dtypes(include=['category']).columns
    for col in cat_cols:
        for old, new in zip(old_val, new_val):
            tmp_df[col] = tmp_df[col].cat.rename_categories({old: new}, **kwargs)

    # For all the other columns use the map method
    non_cat_cols = tmp_df.select_dtypes(exclude=['category']).columns
    for col in non_cat_cols:
        for old, new in zip(old_val, new_val):
            tmp_df[col].replace(old, new, inplace=True, **kwargs)

    return tmp_df

@data_op
def rename_val_in_clm(df: pd.DataFrame,
                       clm:     Optional[List[str]] = None,
                       old_val: Optional[List[str]] = None,
                       new_val: Optional[List[str]] = None,
                       **kwargs) -> pd.DataFrame:
    """rename_val_in_clm.
    Rename the values of a column in the dataframe.

    Parameters
    ----------
    df : pd.DataFrame
        The input data
    clm : List[str]
        List of clms where to apply the value rename
    old_val : List[str]
        List of old values
    new_val : List[str]
        List of new values
    kwargs : Dict
        Dictionary of keyword arguments

    Returns
    -------
    pd.DataFrame
        The renamed DataFrame
    """
    clm = clm if not clm is None else []
    old_val = old_val if not old_val is None else []
    new_val = new_val if not new_val is None else []

    tmp_df = df.copy()
    for old, new in zip(old_val, new_val):
        tmp_df[clm].replace(old, new, inplace=True, **kwargs)
    return tmp_df

@data_op
def replace_nan(df: pd.DataFrame,
                new_val: Any = None,
                **kwargs) -> pd.DataFrame:
    df.fillna(new_val, inplace=True)
    return df

