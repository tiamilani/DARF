# © 2025 Nokia
# Licensed under the BSD 3-Clause License
# SPDX-License-Identifier: BSD-3-Clause
#
# Contact: Mattia Milani (Nokia) <mattia.milani@nokia.com>

"""
split Module
============

Contains operations relatives to the split of dataframes clm/rws
"""

from typing import List, Optional

import pandas as pd

from darf.src.decorators import data_op

@data_op
def split_clm(df: pd.DataFrame,
              clm: str = "",
              separator: str = "_",
              new_clms: Optional[List[str]] = None,
              **kwargs) -> pd.DataFrame:
    """split_clm.
    Split a column into multiple columns based on a separator.

    Parameters
    ----------
    df : pd.DataFrame
        The input data
    clm : str
        The column to split
    separator : str
        The separator to split the column
    new_clms : List[str]
        List of new column names
    kwargs : Dict
        Dictionary of keyword arguments

    Returns
    -------
    pd.DataFrame
        The DataFrame with the split columns
    """
    new_clms = new_clms if new_clms else []

    assert len(new_clms) > 0
    if 'n' in kwargs:
        kwargs['n'] = int(kwargs['n'])
    split = df[clm].str.split(separator, expand=True, **kwargs)
    split.columns = new_clms
    tmp_df = df.drop(columns=[clm])
    return pd.concat([tmp_df, split], axis=1)
