# © 2025 Nokia
# Licensed under the BSD 3-Clause License
# SPDX-License-Identifier: BSD-3-Clause
#
# Contact: Mattia Milani (Nokia) <mattia.milani@nokia.com>

"""
timeseries Module
=============

Contains operations relatives to the timeseries and timestamp domanin.
"""

from typing import List, Any, Optional, Union

import numpy as np
import pandas as pd

from darf.src.decorators import data_op

@data_op
def add_timestamp(df: pd.DataFrame,
                  clm_name: str = "timestamp",
                  start: str = None,
                  end: str = None,
                  delta: int = 1,
                  repeat: Union[int, None, str] = None) -> pd.DataFrame:
    """add_timestamp.

    Add a new timestamp column to the dataset.
    If both no start and end are provided an error is raised.
    If just end is provided the start is set to current datetime.
    If just start is provided the end is set to current datetime.
    If delta is not provided it defaults to 1 second.
    If repeat is not provided then the number of timestamps is equal to the
    length of the dataset, if this is not the case the an error it raised.
    If repeat is set to 'auto' then the legth of the dataset is divided by
    the number of timestamps (given by the delta) and the result is used as
    repeat value. The sequence of timestamps is then repeated accordingly
    and applied. If the division gives a not integer value then an error is
    raised.

    Parameters
    ----------
    df : pd.DataFrame
        The input data
    clm_name : str
        The name of the new timestamp column, default 'timestamp'
    start : str
        The start date time
    end : str
        The end date time
    delta : int
        The time delta between timestamps, default 1
    repeat : Union[int, None, str]
        The number of times the sequence of timestamps should be repeated,
        default None

    Returns
    -------
    pd.DataFrame
        The DataFrame with the new timestamp column

    Raises
    ------
    ValueError
        If the start and end are not provided
    ValueError
        If the repeat value is not valid
    """
    if start is None and end is None:
        raise ValueError("Either start or end must be provided")

    start = pd.Timestamp(start) if start is not None else pd.Timestamp.now()
    end = pd.Timestamp(end) if end is not None else pd.Timestamp.now()
    n_timestamps = int((end - start).total_seconds() / delta) + 1
    delta = pd.Timedelta(seconds=delta)

    # Compute if repetitions are needed
    if repeat is None:
        repeat = 1
    elif repeat == "auto":
        repeat = len(df) / n_timestamps
        if repeat % 1 != 0:
            raise ValueError("The number of timestamps is not a multiple of the dataset length")
    repeat = int(repeat)

    # Generate the list of timestamps
    timestamps = pd.date_range(start=start, end=end, freq=delta)

    # Apply the sequence of timestamps to the dataset
    timestamps = np.tile(timestamps.to_numpy(), repeat)
    df[clm_name] = timestamps
    return df

@data_op
def date_time_filter(df: pd.DataFrame,
                     clm: str = "",
                     start: str = "",
                     end: str = "",
                     **kwargs) -> pd.DataFrame:
    """date_time_filter.
    Filter the dataframe based on a date time column.

    Parameters
    ----------
    df : pd.DataFrame
        The input data
    clm : str
        The column to filter
    start : str
        The start date time
    end : str
        The end date time
    kwargs : Dict
        Dictionary of keyword arguments

    Returns
    -------
    pd.DataFrame
        The filtered DataFrame
    """
    return df[(df[clm] >= start) & (df[clm] <= end)]

@data_op
def clm_to_datetime(df: pd.DataFrame,
                    clm: Optional[List[str]] = None,
                    **kwargs) -> pd.DataFrame:
    """clm_to_datetime.
    Convert columns to datetime

    Parameters
    ----------
    df : pd.DataFrame
        The input data
    clm : List[str]
        List of columns to convert to datetime
    kwargs : Dict
        Dictionary of keyword arguments

    Returns
    -------
    pd.DataFrame
        The DataFrame with the columns converted to datetime
    """
    clm = clm if not clm is None else []
    df[clm] = df[clm].apply(pd.to_datetime, **kwargs)
    return df

@data_op
def flag_first_alert(df: pd.DataFrame,
                     alert_clm: str = "label",
                     alert_id: Any = 1,
                     time_clm: str = "timestamp",
                     delta: int = 60,
                     new_clm: str = "Alert") -> pd.DataFrame:
    """flag_first_alert.

    Function used to flag the first allert detected in <alert_clm> column.
    An alert is detected when the value is equal to <alert_id>.
    An alert is considered new when at least <delta> seconds have passed
    using the <time_clm> column as reference.

    Parameters
    ----------
    df : pd.DataFrame
        The input data
    alert_clm : str
        The column where the alerts are stored
    alert_id : Any
        The value that identifies an alert
    time_clm : str
        The column where the timestamps are stored
    delta : int
        The time delta in seconds
    new_clm : str
        The new column where the flag is stored

    Returns
    -------
    pd.DataFrame
        The DataFrame with the new column
    """
    df[new_clm] = 0

    # Get the indexes of the alerts
    alerts = df[df[alert_clm] == alert_id].index
    if len(alerts) == 0:
        return df

    # Get the indexes of the first alert
    first_alert = alerts[0]
    df.loc[first_alert, new_clm] = 1

    # Get the indexes of the alerts that are at least delta seconds away
    # From the latest alert
    for alert in alerts[1:]:
        if (df.loc[alert, time_clm] - df.loc[first_alert, time_clm]).total_seconds() >= delta:
            df.loc[alert, new_clm] = 1
        first_alert = alert

    return df
