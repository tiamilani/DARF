# © 2025 Nokia
# Licensed under the BSD 3-Clause License
# SPDX-License-Identifier: BSD-3-Clause
#
# Contact: Mattia Milani (Nokia) <mattia.milani@nokia.com>

"""
Save Module
===========

Operations to save a dataframe to a file.
"""

from typing import List, Optional

import pandas as pd

from darf.src.decorators import data_op

@data_op
def save_csv(df: pd.DataFrame,
              file_path: str,
              **kwargs) -> pd.DataFrame:
        """save_csv.
        Save a DataFrame to a CSV file.

        Parameters
        ----------
        df : pd.DataFrame
            The input data
        file_path : str
            The path to the output CSV file
        kwargs : Dict
            Dictionary of keyword arguments

        Returns
        -------
        pd.DataFrame
            The DataFrame with the split columns
        """
        df.to_csv(file_path, index=False, **kwargs)
        return df