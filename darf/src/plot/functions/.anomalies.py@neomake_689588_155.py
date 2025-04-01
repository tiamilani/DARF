# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright (C) 2025 Mattia Milani <mattia.milani@nokia.com>

from typing import Optional
import pandas as pd
import seaborn as sns
import matplotlib as mplt
from seacoral.src.decorators.decorators import plot

@plot
def line_with_anomalies(*args, data: pd.DataFrame = None,
                        anomalies_column: Optional[str] = None,
                        anomalies_reference: Optional[str] = None,
                        **kwargs) -> mplt.axes.Axes:
    """line.

    Parameters
    ----------
    args :
        args
    data : pd.DataFrame
        data
    kwargs :
        kwargs

    Returns
    -------
    mplt.axes.Axes

    """
    if anomalies_column is None:
        raise ValueError("Anomalies column is required")
    if anomalies_reference is None:
        raise ValueError("Anomalies reference is required")
    # p = sns.lineplot(data=data, *args, **kwargs)
    # Vertical line where anomalies column is true
    for i in data[data[anomalies_column] == 1][anomalies_reference].unique():
        p.axvline(i, color='r', linestyle='--')
    return p

