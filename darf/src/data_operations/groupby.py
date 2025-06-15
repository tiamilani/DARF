# © 2025 Nokia
# Licensed under the BSD 3-Clause License
# SPDX-License-Identifier: BSD-3-Clause
#
# Contact: Mattia Milani (Nokia) <mattia.milani@nokia.com>

"""
aggregate Module
================

Contains operations relatives to the aggregation of dataframes clm/rws
"""

from typing import List, Optional, Dict, Any

import pandas as pd

from darf.src.decorators import data_op

@data_op
def groupby(df: pd.DataFrame,
            columns: List[str] = [],
            apply: Optional[str] = None,
            apply_kwargs: Optional[Dict[str, Any]] = None,
            pivot: bool = True,
            reset_index: bool = True) -> pd.DataFrame:
    """groupby.

    Group by the columns and return the number of rows in each group

    Parameters
    ----------
    df : pd.DataFrame
        The input data
    columns : List[str]
        The columns to group by
    apply : str
        The function to apply to the group
    apply_kwargs : Optional[Dict[str, Any]]
        The keyword arguments to pass to the function

    Returns
    -------
    pd.DataFrame
        a pivot version of the input data where for each group there
        is the number of rows in the group
    """
    tmp_df = df.groupby(columns)
    if apply_kwargs is None:
        apply_kwargs = {}

    if apply is None:
        raise ValueError("apply function is required")

    match apply:
        case "first":
            tmp_df = tmp_df.first(**apply_kwargs)
        case "sum":
            tmp_df = tmp_df.sum(**apply_kwargs)
        case "mean":
            tmp_df = tmp_df.mean(**apply_kwargs)
        case "min":
            tmp_df = tmp_df.min(**apply_kwargs)
        case "max":
            tmp_df = tmp_df.max(**apply_kwargs)
        case "count":
            tmp_df = tmp_df.count(**apply_kwargs)
        case _:
            raise ValueError(f"Unknown apply function: {apply}")
    # pivot tmp_df
    if pivot:
        tmp_df = tmp_df.melt(id_vars=columns, value_vars=['count'],
                             var_name='count', value_name='count')
    if reset_index:
        tmp_df = tmp_df.reset_index()
    return tmp_df

@data_op
def groupby_count(df: pd.DataFrame,
                  columns: List[str] = [],
                  count_unique: str = "count_clm",
                  pivot: bool = True) -> pd.DataFrame:
    """grouby_count.

    Group by the columns and count the number of unique
    values in the column `count_unique`

    Parameters
    ----------
    df : pd.DataFrame
        The input data
    columns : List[str]
        The columns to group by
    count_unique : str
        The column where to count the number of unique values

    Returns
    -------
    pd.DataFrame
        a pivot version of the input data where for each group there
        is the count of unique values in the column `count_unique`
    """
    labels = df[count_unique].unique()
    tmp_df = df.groupby(columns)[count_unique].value_counts().unstack().fillna(0).reset_index()
    # pivot tmp_df
    if pivot:
        tmp_df = tmp_df.melt(id_vars=columns, value_vars=labels,
                             var_name=count_unique, value_name="count")
    return tmp_df

@data_op
def groupby_avg(df: pd.DataFrame,
                columns: List[str] = [],
                avg_clm: str = "avg_clm",
                pivot: bool = True) -> pd.DataFrame:
    """groupby_avg.

    Group by the columns and calculate the average of the column `avg_clm`

    Parameters
    ----------
    df : pd.DataFrame
        The input data
    columns : List[str]
        The columns to group by
    avg_clm : str
        The column where to calculate the average

    Returns
    -------
    pd.DataFrame
        a pivot version of the input data where for each group there
        is the average of the column `avg_clm`
    """
    tmp_df = df.groupby(columns)[avg_clm].mean().reset_index()
    # pivot tmp_df
    if pivot:
        tmp_df = tmp_df.melt(id_vars=columns, value_vars=[avg_clm],
                             var_name=avg_clm, value_name="avg")
    return tmp_df

@data_op
def groupby_cm(df: pd.DataFrame,
                columns: List[str] = [],
                pivot: bool = True) -> pd.DataFrame:
    """groupby_cm.

    Group by the columns and calculate the confusion matrix

    Parameters
    ----------
    df : pd.DataFrame
        The input data
    columns : List[str]
        The columns to group by

    Returns
    -------
    pd.DataFrame
        a pivot version of the input data where for each group there
        is the confusion matrix
    """
    exp_clm = "exp_id"
    eval_clm = "Evaluation"
    val_clm = "Value"
    statistic_clm = "Statistic"
    exp_p = "expected_P"
    exp_n = "expected_N"

    cm_df = pd.DataFrame(columns=["exp_id", "Evaluation", "Value", "Statistic"])

    for exp in df[exp_clm].unique():
        tmp_df = df[df[exp_clm] == exp]
        for eval in tmp_df[eval_clm].unique():
            tmp_tmp_df = tmp_df[tmp_df[eval_clm] == eval]
            total_expected_p = tmp_tmp_df[tmp_tmp_df[statistic_clm] == exp_p][val_clm].sum()
            total_expected_n = tmp_tmp_df[tmp_tmp_df[statistic_clm] == exp_n][val_clm].sum()
            total_TP = tmp_tmp_df[tmp_tmp_df[statistic_clm] == "TP"][val_clm].sum()
            total_TN = tmp_tmp_df[tmp_tmp_df[statistic_clm] == "TN"][val_clm].sum()
            total_FP = tmp_tmp_df[tmp_tmp_df[statistic_clm] == "FP"][val_clm].sum()
            total_FN = tmp_tmp_df[tmp_tmp_df[statistic_clm] == "FN"][val_clm].sum()
            cm_df = pd.concat([cm_df, pd.DataFrame({
                exp_clm: [exp, exp, exp, exp],
                eval_clm: [eval, eval, eval, eval],
                statistic_clm: ["TP", "TN", "FP", "FN"],
                val_clm: [total_TP/total_expected_p,
                          total_TN/total_expected_n,
                          total_FP/total_expected_n,
                          total_FN/total_expected_p]
            })], ignore_index=True)
    return cm_df

@data_op
def groupby_cm_avg_std(df: pd.DataFrame,
                pivot: bool = True) -> pd.DataFrame:
    """groupby_cm_avg_std.

    Group by the columns and calculate the confusion matrix

    Parameters
    ----------
    df : pd.DataFrame
        The input data
    columns : List[str]
        The columns to group by

    Returns
    -------
    pd.DataFrame
        a pivot version of the input data where for each group there
        is the confusion matrix
    """
    stat_clm = "Statistic"
    val_clm = "Value"

    means = df.groupby(stat_clm)[val_clm].mean().reset_index()
    std = df.groupby(stat_clm)[val_clm].std().reset_index()
    new_df = pd.merge(means, std, on=stat_clm)
    new_df.columns=[stat_clm, "Mean", "Std"]
    return new_df

@data_op
def groupby_by_day(df: pd.DataFrame,
                     columns: List[str] = [],
                     value_clm: str = "value",
                     pivot: bool = True,
                     reset_index: bool = True) -> pd.DataFrame:
    """groupby_by_day.

    Use the columns to group by the data and return the number total number
    compute as the sum of value_clm for each day

    Parameters
    ----------
    df : pd.DataFrame
        The input data
    columns : List[str]
        The columns to group by
    value_clm : str
        The column where to compute the sum
    pivot : bool
        If True, pivot the dataframe
    reset_index : bool
        If True, reset the index of the dataframe

    Returns
    -------
    pd.DataFrame
        a pivot version of the input data where for each group there
        is the sum of the value_clm for each day
    """
    df = df.groupby(pd.Grouper(key=columns[0], axis=0,
                          freq='1D', sort=True)).sum()
    if reset_index:
        df = df.reset_index()

    return df