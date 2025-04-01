# © 2025 Nokia
# Licensed under the BSD 3-Clause License
# SPDX-License-Identifier: BSD-3-Clause
#
# Contact: Mattia Milani (Nokia) <mattia.milani@nokia.com>

"""
expand Module
=============

Contains operations relatives to the expansion of a dataframe
"""

from typing import List, Any, Optional

import numpy as np
import pandas as pd

from darf.src.decorators import data_op

@data_op
def add_column(df: pd.DataFrame,
               new_clm: str = "new_clm",
               value: Any = 0) -> pd.DataFrame:
    """add_column.
    Add a new column to the DataFrame

    Parameters
    ----------
    df : pd.DataFrame
        The input data
    new_clm : str
        The name of the new column
    value : Any
        The value of the new column

    Returns
    -------
    pd.DataFrame
        The DataFrame with the new column
    """
    tmp_df = df.copy()
    tmp_df[new_clm] = value
    return tmp_df

@data_op
def add_eval_column(df: pd.DataFrame,
                      id_clm: str = "exp_id",
                      eval_clm: str = "eval",
                      start_val: int = 0) -> pd.DataFrame:
    """append_eval_cycle.
    Append the evaluation cycle to the DataFrame.
    The 'eval_clm' will be appended as new column to the dataframe.
    The value of this column will be equal to 'start_val' for the first
    unique occurence of each 'id_clm' element and then increase for each
    repeated occurence.

    Parameters
    ----------
    df : pd.DataFrame
        The input data
    id_clm : str
        The column that identifies the group of elements
    eval_clm : str
        The column to append
    start_val : int
        The starting value for the evaluation cycle

    Returns
    -------
    pd.DataFrame
        The DataFrame with the appended evaluation cycle
    """
    tmp_df = df.copy()
    unique_ids = tmp_df[id_clm].unique()
    eval_cycle = np.zeros(len(tmp_df))
    for local_id in unique_ids:
        mask = tmp_df[id_clm] == local_id
        eval_cycle[mask] = np.arange(start_val, start_val+len(tmp_df[mask]))
    eval_cycle = eval_cycle.astype(np.int8)
    tmp_df[eval_clm] = eval_cycle
    return tmp_df

@data_op
def curriculum_include_expected_columns(df: pd.DataFrame,
                                        all_n: bool = True,
                                        sum_clm: Optional[List[str]] = None,
                                        new_clm: Optional[List[str]] = None) -> pd.DataFrame:
    """curriculum_include_expected_columns.
    Sum the values in 'sum_clm' in order to obtain the values for 'new_clm'
    if AllN then the sum is saved in new_clm[2] ('expected_N').
    Otehrwise raise not_implemented error

    Parameters
    ----------
    df : pd.DataFrame
        The input data
    AllN : bool
        Flag to compute the expected_N value
    sum_clm : List[str]
        List of columns to sum
    new_clm : List[str]
        List of new columns

    Returns
    -------
    pd.DataFrame
        The DataFrame with the new columns
    """
    sum_clm = sum_clm if not sum_clm is None else []
    new_clm = new_clm if not new_clm is None else ["expected_P", "expected_N"]

    if not all_n:
        raise NotImplementedError("Not implemented yet")

    tmp_df = df.copy()
    tmp_df[new_clm[1]] = tmp_df[sum_clm].sum(axis=1)
    tmp_df[new_clm[0]] = 0
    return tmp_df

@data_op
def add_trigger(df: pd.DataFrame,
                id_clm: str = "exp_id",
                val_clm: str = "value",
                new_clm: str = "Trigger",
                threshold: float = 0.5,
                histeresis_until: Optional[float] = None,
                outer_drop: bool = False,
                inner_drop: bool = False) -> pd.DataFrame:
    """add_trigger.

    This function adds a new colum identified by `new_clm` to the DataFrame.
    The new column contains the information about if a threshold has been
    triggered or not.
    The possible value are:
        - `start` when the first value above the threshold is detected
        - `end` when the value goes below the `histeresis_until` value
        - `triggered` between the `start` and `end` values
        - `none` if the threshold is not reached and the current row is outside
            a `start` and `end` couple
    If the `histeresis_until` is `None` (default) then the value is equal to the
    threshold.

    Is possible to automatically drop the rows outside the trigger range using
    the `outer_drop` flag.
    Is possible to automatically drop the rows inside the trigger range using
    the `inner_drop` flag.

    Parameters
    ----------
    df : pd.DataFrame
        The input data
    id_clm : str
        The column that identifies the group of elements
    val_clm: str
        The column where to apply the trigger
    new_clm : str
        The column to append
    threshold : float
        The threshold value
    histeresis_until : float
        The histeresis value
    outer_drop : bool
        Flag to drop the rows outside the trigger range
    inner_drop : bool
        Flag to drop the rows inside the trigger range

    Returns
    -------
    pd.DataFrame
        The DataFrame with the appended trigger column
    """
    ret_df = None

    histeresis = histeresis_until if not histeresis_until is None else threshold

    if len(df) >= 1000000:
        raise Exception("The function `add_trigger` is not optimized for large DataFrames!")

    for id in df[id_clm].unique():
        tmp_df = df[df[id_clm] == id].copy()
        tmp_df[new_clm] = "none"
        in_trigger = False
        for row in tmp_df.iterrows():
            idx = row[0]
            row = row[1]
            if not in_trigger and row[val_clm] < threshold:
                pass

            if not in_trigger and row[val_clm] >= threshold:
                tmp_df.loc[idx, new_clm] = "start"
                in_trigger = True
            elif in_trigger and row[val_clm] < histeresis:
                tmp_df.loc[idx, new_clm] = "end"
                in_trigger = False
            elif in_trigger:
                tmp_df.loc[idx, new_clm] = "Triggered"

        # Drop the rows outside the trigger range
        if outer_drop:
            outer_mask = (tmp_df[new_clm] == "none")
            tmp_df = tmp_df[~outer_mask]

        # Drop the rows inside the trigger range
        if inner_drop:
            inner_mask = (tmp_df[new_clm] == "Triggered")
            tmp_df = tmp_df[~inner_mask]

        if ret_df is None:
            ret_df = tmp_df
        else:
            ret_df = pd.concat([ret_df, tmp_df])

    print(ret_df)
    raise Exception("Stop")

    return ret_df
