# © 2025 Nokia
# Licensed under the BSD 3-Clause License
# SPDX-License-Identifier: BSD-3-Clause
#
# Contact: Mattia Milani (Nokia) <mattia.milani@nokia.com>

"""
Transform Module
================

Contains operations relatives to the transformation of a dataframe
"""

from typing import List, Optional

import pandas as pd
import umap.umap_ as umap
from sklearn.preprocessing import StandardScaler

from darf.src.decorators import data_op

@data_op
def umap2df(df: pd.DataFrame,
            in_clm: Optional[List[str]] = None,
            columns: Optional[List[str]] = None,
            **kwargs) -> pd.DataFrame:
    """umap2df.
    Apply an umap transformation to the dataframe

    Parameters
    ----------
    df : pd.DataFrame
        df where to apply the umap
    in_clm : Optional[List[str]]
        in_clm to apply the umap
    columns : List[str]
        output columns for umap
    kwargs :
        kwargs to pass to umap.UMAP

    Returns
    -------
    pd.DataFrame

    """
    columns = columns if not columns is None else ['X', 'Y']
    in_clm = in_clm if not in_clm is None else []

    emb = df[in_clm].values if not in_clm is None else df.values
    reducer = umap.UMAP(n_neighbors=30, min_dist=0.0, **kwargs)
    scaled_data = StandardScaler().fit_transform(emb)
    embedding = reducer.fit_transform(scaled_data)
    result = pd.DataFrame(embedding, columns=columns)

    # Delete the in_clm from the df
    if in_clm is None:
        return result
    df.drop(in_clm, axis=1, inplace=True)

    # Reset indexes
    df.reset_index(drop=True, inplace=True)
    result.reset_index(drop=True, inplace=True)

    # Join df and result
    result = pd.concat([df, result], axis=1)

    result[columns] = result[columns].apply(pd.to_numeric)
    return result

@data_op
def set_index(df: pd.DataFrame, *args, **kwargs) -> pd.DataFrame:
    """set_index.
    Set the index of the DataFrame

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
        The DataFrame with the index set
    """
    print(args)
    print(kwargs)
    return df.set_index(*args, **kwargs)
