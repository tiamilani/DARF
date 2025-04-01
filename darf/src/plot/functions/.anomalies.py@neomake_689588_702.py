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
import datetime
import pandas as pd
import seaborn as sns
import matplotlib as mplt
import matplotlib.dates as mdates
from seacoral.src.decorators.decorators import plot

@plot
def line_with_anomalies(*args, data: pd.DataFrame = None,
                        anomalies_column: Optional[str] = None,
                        anomalies_reference: Optional[str] = None,
                        **kwargs) -> mplt.axes.Axes:
    """line.

    Plot a lineplot with vertical lines that marks anomalies

    Parameters
    ----------
    args :
        args
    data : pd.DataFrame
        data
    anomalies_column: str
        column that contains the anomalies
    anomalies_reference: str
        column that contains the reference for the anomalies (datetime)
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
    p = sns.lineplot(data=data, *args, **kwargs)
    # Vertical line where anomalies column is true
    for i in data[data[anomalies_column] == 1][anomalies_reference].unique():
        p.axvline(i, color='r', linestyle='--')
    mplt.pyplot.gca().xaxis.set_major_formatter(mdates.DateFormatter("%d-%b"))
    mplt.pyplot.gca().xaxis.set_major_locator(mdates.DayLocator(interval=7))
    # freq = 7
    # all_dates = data["timestamp"].unique()
    # frq_dates = data["timestamp"].dt.strftime("%d-%b").unique()[::freq]
    # mplt.pyplot.gca().set_xticks(range(len(all_dates))[::freq*24*60], labels=frq_dates)
    # x_ticks= [data.iloc[::freq]["timestamp"][:5].dt.strftime("%d-%b").values]
    # mplt.pyplot.gca().set_xticklabels(x_ticks)
    # # set the xticks at the same frequency as the xlabels
    # xtix = mplt.pyplot.gca().get_xticks()
    # mplt.pyplot.gca().set_xticks(xtix[::freq][:5])
    # #nicer label format for dates
    p.get_figure().autofmt_xdate()
    return p

@plot
def line_outages_description(*args, data: pd.DataFrame = None,
                             anomalies_column: Optional[str] = None,
                             anomalies_reference: Optional[str] = None,
                             date_formatter_format: Optional[str] = "%d-%b %H:%M",
                             hour_locator_kwargs: Optional[dict] = None,
                             **kwargs) -> mplt.axes.Axes:
    """line_outages_description.

    Lineplot for outages

    """
    if anomalies_column is None:
        raise ValueError("Anomalies column is required")
    if anomalies_reference is None:
        raise ValueError("Anomalies reference is required")
    p = sns.lineplot(data=data, *args, **kwargs)
    p2 = sns.lineplot(data, x='timestamp', y='Value',
                      hue='Statistic', hue_order=['bad_p'],
                      palette=['red'], ax=p.axes.twinx())
    p2.axhline(50, color='r', linestyle='--')
    # Vertical line where anomalies column is true
    # for i in data[data[anomalies_column] == 1][anomalies_reference].unique():
    #     p.axvline(i, color='r', linestyle='--')
    mplt.pyplot.gca().xaxis.set_major_formatter(mdates.DateFormatter(date_formatter_format))
    mplt.pyplot.gca().xaxis.set_major_locator(mdates.HourLocator(**hour_locator_kwargs))
    p.figure.autofmt_xdate()
    return p

@plot
def line_outages_alerts(*args, data: pd.DataFrame = None,
                        anomalies_column: Optional[str] = None,
                        anomalies_reference: Optional[str] = None,
                        date_formatter_format: Optional[str] = "%d-%b %H:%M",
                        hour_locator_kwargs: Optional[dict] = None,
                        stat_clm: Optional[str] = "Statistic",
                        heatmap_prop: Optional[str] = "bad_p",
                        **kwargs) -> mplt.axes.Axes:
    """line_outages_description.

    Lineplot for outages

    """
    if anomalies_column is None:
        raise ValueError("Anomalies column is required")
    if anomalies_reference is None:
        raise ValueError("Anomalies reference is required")

    fig, axes = mplt.pyplot.subplots(2,1, gridspec_kw={'height_ratios': [8, 1]})

    p = sns.lineplot(data=data, ax=axes[0], *args, **kwargs)
    axes[1].imshow(data[data[stat_clm] == heatmap_prop][kwargs['y']].values.reshape(1, -1), aspect='auto', cmap='RdYlGn', vmin=0, vmax=1)
    axes[1].set_yticks([0], labels=['Outage prob.'])
    axes[1].set_xticks([])
    axes[1].set_xticks([], minor=True)
    for i in data[data[anomalies_column] == 1][anomalies_reference].unique():
        p.axvline(i, color='r', linestyle='--')
    axes[1].xaxis.set_major_formatter(mdates.DateFormatter(date_formatter_format))
    axes[1].xaxis.set_major_locator(mdates.HourLocator(**hour_locator_kwargs))
    p.figure.autofmt_xdate()
    return p
