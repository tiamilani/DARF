# © 2025 Nokia
# Licensed under the BSD 3-Clause License
# SPDX-License-Identifier: BSD-3-Clause
#
# Contact: Mattia Milani (Nokia) <mattia.milani@nokia.com>

from typing import Optional
import datetime
import pandas as pd
import seaborn as sns
import matplotlib as mplt
import matplotlib.dates as mdates
from darf.src.decorators.decorators import plot

@plot
def anomalies_prob_heatmap(pvt_kwargs=None, htm_kwargs=None,
                           data: pd.DataFrame = None,
                           date_formatter_format: Optional[str] = "%d-%b",
                           hour_locator_kwargs: Optional[dict] = None,
                           **kwargs) -> mplt.axes.Axes:
    """anomalies_prob_heatmap.

    Apply a heatmap to the data and also pivot the dataset
    This function is intended to be used on anomalies datasets, which
    contains a timestamp x column.

    Parameters
    ----------
    pvt_kwargs :
        pvt_kwarg
    htm_kwargs :
        htm_kwarg
    kwargs :
        kwargs
    """

    # If the palette kwarg is present then remove it
    if 'palette' in kwargs:
        kwargs.pop('palette')

    pivot_data = data.pivot(**pvt_kwargs)
    p = sns.heatmap(data=pivot_data, **htm_kwargs, **kwargs)
    mplt.pyplot.gca().tick_params(axis='y', rotation=45)
    return p


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
    prob = sns.lineplot(data=data, x=kwargs['x'], y=kwargs['y'],
                        ax=axes[1], hue=stat_clm, hue_order=[heatmap_prop],
                        palette=['red'])
    axes[1].set_ylabel('Outage prob.')
    axes[1].set_ylim(0, 100)
    # Remove axes[1] legend
    axes[1].get_legend().remove()

    top_y = p.get_ylim()[1]
    for i in data[data[anomalies_column] == 1][anomalies_reference].unique():
        p.axvline(i, color='r', linestyle='--')
        p.text(i+datetime.timedelta(minutes = 10), top_y*0.85, f"{i.strftime('%H:%M')}")
    mplt.pyplot.gca().xaxis.set_major_formatter(mdates.DateFormatter(date_formatter_format))
    mplt.pyplot.gca().xaxis.set_major_locator(mdates.HourLocator(**hour_locator_kwargs))
    p.figure.autofmt_xdate()
    return p

@plot
def line_outages_alerts_distances(*args, data: pd.DataFrame = None,
                                  kpi_kwargs: Optional[dict] = None,
                                  prb_kwargs: Optional[dict] = None,
                                  dst_kwargs: Optional[dict] = None,
                                  **kwargs) -> mplt.axes.Axes:
    """line_outages_description.

    Lineplot for outages

    """
    fig, axes = mplt.pyplot.subplots(3,1, gridspec_kw={'height_ratios': [4, 3, 3]})

    # Check if a palette is present in the kwargs
    if 'palette' in kwargs:
        palette = kwargs.pop('palette')

    if 'palette' not in kpi_kwargs:
        kpi_kwargs['palette'] = palette
    if 'palette' not in prb_kwargs:
        prb_kwargs['palette'] = palette
    if 'palette' not in dst_kwargs:
        dst_kwargs['palette'] = palette

    p = sns.lineplot(data=data, ax=axes[0], *args, **kpi_kwargs, **kwargs)
    prob = sns.lineplot(data=data, ax=axes[1], *args, **prb_kwargs, **kwargs)
    dst = sns.lineplot(data=data, ax=axes[2], *args, **dst_kwargs, **kwargs)
    return p

@plot
def line_outage_dst(*args, data: pd.DataFrame = None,
                    prb_kwargs: Optional[dict] = None,
                    dst_kwargs: Optional[dict] = None,
                    **kwargs) -> mplt.axes.Axes:
    """line_outages_description.

    Lineplot for outages

    """
    fig, axes = mplt.pyplot.subplots(2,1, gridspec_kw={'height_ratios': [5, 5]})

    # Check if a palette is present in the kwargs
    if 'palette' in kwargs:
        palette = kwargs.pop('palette')

    if 'palette' not in prb_kwargs:
        prb_kwargs['palette'] = palette
    if 'palette' not in dst_kwargs:
        dst_kwargs['palette'] = palette

    prob = sns.lineplot(data=data, ax=axes[0], *args, **prb_kwargs, **kwargs)
    dst = sns.lineplot(data=data, ax=axes[1], *args, **dst_kwargs, **kwargs)
    return prob
