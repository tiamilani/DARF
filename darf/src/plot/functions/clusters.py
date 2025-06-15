# © 2025 Nokia
# Licensed under the BSD 3-Clause License
# SPDX-License-Identifier: BSD-3-Clause
#
# Contact: Mattia Milani (Nokia) <mattia.milani@nokia.com>

"""
clusters plot functions module
==============================

This module contains functions to plot easily clusters.
"""

from typing import Any, Dict, List
import pandas as pd
import seaborn as sns
import matplotlib as mplt
from darf.src.decorators.decorators import plot

# pylint: disable=unused-variable

@plot
def multi_joint(*args, data: pd.DataFrame = None,
                colors_scatter: List[str] = None,
                scatter_kwargs: Dict[str, Any] = None,
                compute_centroids: bool = False,
                **kwargs) -> None:
    """multi_joint.

    Special function to apply a scatterplot on top of jointplot

    Parameters
    ----------
    args :
        args for the jointplot
    data : pd.DataFrame
        data
    colors_scatter : List[str]
        colors_scatter for the scatterplot
    scatter_kwargs : Dict[str, Any]
        scatter_kwargs for the scatterplot
    kwargs :
        kwargs

    Returns
    -------
    None

    """
    # data['Label'] = data['Label'].astype('category')
    # print(data.dtypes)
    # print(data)
    p_joint = sns.kdeplot(data=data, *args, **kwargs)

    if compute_centroids:
        # Extract hue_order labels point from the data
        hue_order = kwargs.get("hue_order", None)
        if hue_order is None:
            hue_order = data["Label"].unique()

        hue_centroids = data[data["Label"].isin(hue_order)].groupby("Label").mean()

        p_joint = sns.scatterplot(data=hue_centroids, x='X', y='Y',
                                  hue="Label", palette=["red", "red"],
                                  style="Label", markers=['X'],
                                  ax=p_joint.figure.get_axes()[0])

    if scatter_kwargs is None:
        return p_joint

    color_plt = sns.color_palette(colors_scatter, as_cmap=True)

    tmp_dat = data.copy()
    if "sub_select" in scatter_kwargs:
        for k, value in scatter_kwargs["sub_select"].items():
            tmp_dat = tmp_dat[tmp_dat[k] == value]
        del scatter_kwargs["sub_select"]

    scatter_plt = sns.scatterplot(data=tmp_dat, palette=color_plt,
                        ax=p_joint.figure.get_axes()[0], **scatter_kwargs)
    # p.plot_joint(sns.scatterplot, data=tmp_dat, palette=cm, **scatter_kwargs)
    return [p_joint, scatter_plt]

@plot
def clusters_sequence(*args, data: pd.DataFrame = None,
                      iterate_clm: str = "Iteration",
                      colors_scatter: Dict[str, Any] = None,
                      scatter_kwargs: Dict[str, Any] = None,
                      colors_centr: Dict[str, Any] = None,
                      scatter_centr_kwargs: Dict[str, Any] = None,
                      scatter_sub_select: Dict[str, str] = None,
                      centr_sub_select: Dict[str, str] = None,
                      **kwargs) -> List[mplt.axes.Axes]:
    iterations = sorted(data[iterate_clm].unique())
    results = []
    for i in iterations:
        tmp_dat = data[data[iterate_clm] == i]
        p_joint = sns.jointplot(data=tmp_dat, *args, **kwargs)

        # color_plt = sns.color_palette(colors_scatter)
        if scatter_kwargs is not None:
            scatter_tmp_dat = tmp_dat.copy()
            if scatter_sub_select is not None:
                for k, value in scatter_sub_select.items():
                    scatter_tmp_dat = scatter_tmp_dat[scatter_tmp_dat[k] == value]

            scatter_plt = sns.scatterplot(data=scatter_tmp_dat,
                                ax=p_joint.ax_joint, **scatter_kwargs)

        if scatter_centr_kwargs is not None:
            centr_tmp_dat = tmp_dat.copy()
            if centr_sub_select is not None:
                # Value might be a list, and need to check with isin
                for k, value in centr_sub_select.items():
                    centr_tmp_dat = centr_tmp_dat[centr_tmp_dat[k].isin(value)]

            scatter_plt = sns.scatterplot(data=centr_tmp_dat,
                                ax=p_joint.ax_joint, **scatter_centr_kwargs)
        results.append(p_joint)
    return results
