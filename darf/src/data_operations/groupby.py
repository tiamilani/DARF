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

from typing import List, Optional

import pandas as pd

from darf.src.decorators import data_op

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
