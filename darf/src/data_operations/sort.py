# © 2025 Nokia
# Licensed under the BSD 3-Clause License
# SPDX-License-Identifier: BSD-3-Clause
#
# Contact: Mattia Milani (Nokia) <mattia.milani@nokia.com>

"""
Sort Module
===========

Operations to save a dataframe to a file.
"""

from typing import List, Optional

import pandas as pd

from darf.src.decorators import data_op

@data_op
def sort(df: pd.DataFrame,
        clm: List[str] = [],
       **kwargs) -> pd.DataFrame:
        """
        sort.
        Sort a DataFrame by the specified columns.

        Parameters
        ----------
        df : pd.DataFrame
                The input data
        clm : List[str], optional
                List of column names to sort by
        kwargs : Dict
                Additional keyword arguments to pass to pd.DataFrame.sort_values

        Returns
        -------
        pd.DataFrame
                The sorted DataFrame
        """
        if not clm:
                return df
        return df.sort_values(by=clm, **kwargs)