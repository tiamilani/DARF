# © 2025 Nokia
# Licensed under the BSD 3-Clause License
# SPDX-License-Identifier: BSD-3-Clause
#
# Contact: Mattia Milani (Nokia) <mattia.milani@nokia.com>

"""
Facetgrid plot operations
=========================

Apply facetgrid functions
"""

from typing import Optional, Dict, Tuple, List, Union, Any

import math
import pandas as pd
import matplotlib as mplt
import matplotlib.patches as patches
import seaborn as sns

from matplotlib.path import Path
from datetime import datetime
from darf.src.decorators import plot_op

@plot_op
def facetgrid_set_titles(df: pd.DataFrame,
                         facetgrid: sns.FacetGrid,
                         **kwargs) -> sns.FacetGrid:
    """facetgrid_set_titles.

    Set the titles to the facetgrid

    Parameters
    ----------
    facetgrid : sns.FacetGrid
        The facetgrid to set the titles
    args:
        args
    kwargs :
        kwargs

    Returns
    -------
    sns.FacetGrid
        The facetgrid with the titles set
    """
    facetgrid.set_titles(**kwargs)
    return facetgrid

@plot_op
def facet_set_ax_ylabel(df: pd.DataFrame,
                        facetgrid: sns.FacetGrid,
                        row_id: int = 0,
                        col_id: int = 0,
                        label: str = "",
                        **kwargs) -> sns.FacetGrid:
    """set_ax_ylabel.

    Set the ylabel to the axis identified by `row_id` and `col_id`

    Parameters
    ----------
    df : pd.DataFrame
        The input data
    facetgrid : sns.FacetGrid
        The facetgrid to set the ylabel
    row_id : int
        The row id
    col_id : int
        The col id
    label : str
        The ylabel
    kwargs :
        kwargs

    Returns
    -------
    sns.FacetGrid
        The facetgrid with the ylabel set
    """
    ax = facetgrid.facet_axis(row_id, col_id)
    ax.set_ylabel(label, **kwargs)
    return facetgrid

@plot_op
def facet_set_ax_xlabel(df: pd.DataFrame,
                        facetgrid: sns.FacetGrid,
                        row_id: Optional[int] = None,
                        col_id: Optional[int] = None,
                        label: str = "",
                        **kwargs) -> sns.FacetGrid:
    """set_ax_ylabel.

    Set the xlabel to the axis identified by `row_id` and `col_id`
    If both `row_id` and `col_id` are provided the xlabel will be set on
    the selcted ax of the FacetGrid.
    If only `row_id` is provided the xlabel will be set on all the axes
    of the row.
    If only `col_id` is provided the xlabel will be set on all the axes
    of the column.
    If neither `row_id` nor `col_id` are provided an the xlabel will be
    set on all the axes.

    Parameters
    ----------
    df : pd.DataFrame
        The input data
    facetgrid : sns.FacetGrid
        The facetgrid to set the ylabel
    row_id : int
        The row id
    col_id : int
        The col id
    label : str
        The ylabel
    kwargs :
        kwargs

    Returns
    -------
    sns.FacetGrid
        The facetgrid with the ylabel set
    """
    if row_id is not None and col_id is not None:
        ax = facetgrid.facet_axis(row_id, col_id)
        ax.set_xlabel(label, **kwargs)

    if row_id is None and col_id is None:
        for ax in facetgrid.axes.flatten():
            ax.set_xlabel(label, **kwargs)

    if row_id is not None:
        axes_row = facetgrid.axes[row_id]
        for ax in axes_row:
            ax.set_xlabel(label, **kwargs)

    if col_id is not None:
        axes_clm = [facetgrid.axes[i][col_id] for i in range(len(facetgrid.axes))]
        for ax in axes_clm:
            ax.set_xlabel(label, **kwargs)

    return facetgrid


@plot_op
def facet_set_row_ylimits(df: pd.DataFrame,
                          facetgrid: sns.FacetGrid,
                          row_id: int = 0,
                          limits: Tuple[float, float] = (0.0, 1.0),
                          **kwargs) -> sns.FacetGrid:
    """set_ax_ylabel.

    Set the ylimits to the axis identified by `row_id`

    Parameters
    ----------
    df : pd.DataFrame
        The input data
    facetgrid : sns.FacetGrid
        The facetgrid to set the ylabel
    row_id : int
        The row id
    limits : Tuple[float, float]
        The ylimits
    kwargs :
        kwargs

    Returns
    -------
    sns.FacetGrid
        The facetgrid with the ylabel set
    """
    axes_row = facetgrid.axes[row_id]

    for ax in axes_row:
        ax.set_ylim(limits, **kwargs)
    return facetgrid

@plot_op
def facet_subplots_adjust(df: pd.DataFrame,
                          facetgrid: sns.FacetGrid,
                          **kwargs) -> sns.FacetGrid:
    """facet_subplots_adjust.

    Adjust the subplots

    Parameters
    ----------
    df : pd.DataFrame
        The input data
    facetgrid : sns.FacetGrid
        The facetgrid to adjust the subplots
    kwargs :
        kwargs

    Returns
    -------
    sns.FacetGrid
        The facetgrid with the subplots adjusted
    """
    facetgrid.fig.subplots_adjust(**kwargs)
    return facetgrid

@plot_op
def facet_add_hline(df: pd.DataFrame,
                    facetgrid: sns.FacetGrid,
                    row_id: Optional[int] = None,
                    clm_id: Optional[int] = None,
                    **kwargs) -> sns.FacetGrid:
    """facet_add_hline.

    Add an horizontal line to the facetgrid, row_id and clm_id controls
    where to apply the horizontal line.
    If only row_id is provided the horizontal line will be added to all
    facet on the row.
    If only clm_id is provided the horizontal line will be added to all
    facet on the column.
    If both row_id and clm_id are provided the horizontal line will be
    added to the specific facet.

    At least one between row_id and clm_id must be provided otherwise an
    exception is raised.

    Parameters
    ----------
    df : pd.DataFrame
        The input data
    facetgrid : sns.FacetGrid
        The facetgrid to add the horizontal line
    row_id : int
        The row id where to apply the horizontal line
    clm_id : int
        The column id where to apply the horizontal line
    kwargs :
        kwargs

    Returns
    -------
    sns.FacetGrid
        The facetgrid with the horizontal line added
    """
    if row_id is None and clm_id is None:
        raise ValueError("At least one between row_id and clm_id must be provided")

    if row_id is not None and clm_id is not None:
        ax = facetgrid.facet_axis(row_id, clm_id)
        ax.axhline(**kwargs)

    if row_id is not None:
        axes_row = facetgrid.axes[row_id]
        for ax in axes_row:
            ax.axhline(**kwargs)

    if clm_id is not None:
        axes_clm = [facetgrid.axes[i][clm_id] for i in range(len(facetgrid.axes))]
        for ax in axes_clm:
            ax.axhline(**kwargs)

    return facetgrid

@plot_op
def facet_remove_extra_y_labels(df: pd.DataFrame,
                                facetgrid: sns.FacetGrid,
                                row_id: Optional[int] = None,
                                **kwargs) -> sns.FacetGrid:
    """facet_remove_extra_y_labels.

    Remove the extra y labels from the facetgrid, keep only the ylabels
    on the first ax for each row.
    If row_id is provided only the ylabels on the row identified by it
    will be modified.
    Otherwise all the rows will be modified.

    Parameters
    ----------
    df : pd.DataFrame
        The input data
    facetgrid : sns.FacetGrid
        The facetgrid to remove the extra y labels
    row_id : int
        The row id where to remove the extra y labels
    kwargs :
        kwargs

    Returns
    -------
    sns.FacetGrid
        The facetgrid with the extra y labels removed
    """
    if row_id is not None:
        axes_row = facetgrid.axes[row_id]
        for ax in axes_row[1:]:
            ax.set_yticklabels([], **kwargs)

    axes = facetgrid.axes
    for ax_row in axes:
        for ax in ax_row[1:]:
            ax.set_yticklabels([], **kwargs)

    return facetgrid

@plot_op
def facet_add_axis_markers(df: pd.DataFrame,
                           facetgrid: sns.FacetGrid,
                           row_id: Optional[int] = None,
                           clm_id: Optional[int] = None,
                           **kwargs) -> sns.FacetGrid:
    """facet_add_axis_markers.

    Add axis markers to the facetgrid, row_id and clm_id controls
    where to apply the markers.
    If only row_id is provided the markers will be added to all
    facet on the row.
    If only clm_id is provided the markers will be added to all
    facet on the column.
    If both row_id and clm_id are provided the markers will be
    added to the specific facet.

    if neither row_id nor clm_id are provided the tick_params operation
    is applied to all the axes.

    Parameters
    ----------
    df : pd.DataFrame
        The input data
    facetgrid : sns.FacetGrid
        The facetgrid to add the markers
    row_id : int
        the row id where to apply the markers
    clm_id : int
        the column id where to apply the markers
    kwargs :
        kwargs

    Returns
    -------
    sns.FacetGrid
        The facetgrid with the markers added
    """
    if row_id is None and clm_id is None:
        axes = facetgrid.axes
        for ax_row in axes:
            for ax in ax_row:
                ax.tick_params(**kwargs)

    if row_id is not None and clm_id is not None:
        ax = facetgrid.facet_axis(row_id, clm_id)
        ax.tick_params(**kwargs)

    if row_id is not None:
        axes_row = facetgrid.axes[row_id]
        for ax in axes_row:
            ax.tick_params(**kwargs)

    if clm_id is not None:
        axes_clm = [facetgrid.axes[i][clm_id] for i in range(len(facetgrid.axes))]
        for ax in axes_clm:
            ax.tick_params(**kwargs)

    return facetgrid

@plot_op
def facet_add_grid(df: pd.DataFrame,
                   facetgrid: sns.FacetGrid,
                   row_id: Optional[int] = None,
                   clm_id: Optional[int] = None,
                   which: str = "both",
                   **kwargs) -> sns.FacetGrid:
    """facet_add_grid.

    Add a grid to the facetgrid axes
    if both row_id and clm_id are provided the grid will be added to the
    specific facet.
    if only row_id is provided the grid will be added to all the axes
    in the row.
    if only clm_id is provided the grid will be added to all the axes
    in the column.
    if neither row_id nor clm_id are provided the grid will be added to
    all the axes.

    Parameters
    ----------
    df : pd.DataFrame
        The input data
    facetgrid : sns.FacetGrid
        The facetgrid to add the grid
    row_id : int
        the row id where to apply the markers
    clm_id : int
        the column id where to apply the markers
    which : str
        which axis to apply the grid, "both", "x" or "y"

    Returns
    -------
    sns.FacetGrid
        The facetgrid with the grid added
    """
    def add_grid(ax, **kwargs):
        match which:
            case "both":
                ax.grid(True, **kwargs)
            case "x":
                ax.xaxis.grid(True, **kwargs)
            case "y":
                ax.yaxis.grid(True, **kwargs)

    if row_id is None and clm_id is None:
        axes = facetgrid.axes.flatten()
        for ax in axes:
            add_grid(ax, **kwargs)

    if row_id is not None and clm_id is not None:
        ax = facetgrid.facet_axis(row_id, clm_id)
        add_grid(ax, **kwargs)

    if row_id is not None:
        axes_row = facetgrid.axes[row_id]
        for ax in axes_row:
            add_grid(ax, **kwargs)

    if clm_id is not None:
        axes_clm = [facetgrid.axes[i][clm_id] for i in range(len(facetgrid.axes))]
        for ax in axes_clm:
            add_grid(ax, **kwargs)

    return facetgrid

@plot_op
def facet_add_title(df: pd.DataFrame,
                    facetgrid: sns.FacetGrid,
                    title: str = "Title",
                    top_adjust: float = 0.9,
                    **kwargs) -> sns.FacetGrid:
    """facet_add_title.

    Add a title to the facetgrid figure

    Parameters
    ----------
    df : pd.DataFrame
        The input data
    facetgrid : sns.FacetGrid
        The facetgrid to add the title
    title : str
        the title to add
    top_adjust : float
        the top adjust for the title

    Returns
    -------
    sns.FacetGrid
        The facetgrid with the title added
    """
    facetgrid.fig.subplots_adjust(top=top_adjust)
    facetgrid.fig.suptitle(title)
    return facetgrid

@plot_op
def facet_add_patches(df: pd.DataFrame,
                      facetgrid: sns.FacetGrid,
                      patches: List[Dict[str, Any]]) -> sns.FacetGrid:
    """facet_add_patches.

    Add patches to the facetgrid axes.
    The patches are defined in the patches list.
    Each patch is a dictionary with the following attributes:
        - `col_id`: The column where to apply the patch
        - `row_id`: NOT SUPPORTED AT THE MOMENT
        - `verts`: The vertices of the patch, is possible to apply special
            vertices keywords, like `y_min` and `y_max` in order to apply
            the same patch to different axes with different limits
        - `codes`: The codes of the patch, same as matplotlib withtout the `Path`
            prepending, e.g. Just write `MOVETO`, `LINETO`, etc.
        - `PathPatch`: Contains the kwargs to pass to the `PathPatch` constructor

    Parameters
    ----------
    df : pd.DataFrame
        The input data
    facetgrid : sns.FacetGrid
        The facetgrid to add the patches
    patches : List[Dict[str, Any]]
        The list of patches to add

    Returns
    -------
    sns.FacetGrid
        The facetgrid with the patches added
    """
    def switch_vert(ax, keyword):
        match keyword:
            case "y_min":
                return ax.get_ylim()[0]
            case "y_max":
                return ax.get_ylim()[1]
            case _:
                if isinstance(keyword, str):
                    try:
                        dt = datetime.strptime(keyword, "%Y-%m-%d %H:%M:%S")
                    except ValueError:
                        return keyword
                    return mplt.dates.date2num(dt)
                return keyword

    def switch_code(code):
        match code:
            case "MOVETO":
                return Path.MOVETO
            case "LINETO":
                return Path.LINETO
            case "CURVE3":
                return Path.CURVE3
            case "CURVE4":
                return Path.CURVE4
            case "CLOSEPOLY":
                return Path.CLOSEPOLY
            case _:
                raise ValueError(f"Code {code} not supported")

    def add_patch(ax, verts, codes, pathpatch_kw):
        verts = [(switch_vert(ax, vert[0]), switch_vert(ax, vert[1])) for vert in verts]
        codes = [switch_code(code) for code in codes]

        path = mplt.path.Path(verts, codes)
        patch = mplt.patches.PathPatch(path, **pathpatch_kw)
        ax.add_patch(patch)

    for patch in patches:
        col_id = patch.get('col_id', None)
        row_id = patch.get('row_id', None)
        verts = patch.get('verts', None)
        codes = patch.get('codes', None)
        pathpatch_kw = patch.get('PathPatch', None)

        # Cycle over the columns
        axes_clm = [facetgrid.axes[i][col_id] for i in range(len(facetgrid.axes))]
        for ax in axes_clm:
            add_patch(ax, verts, codes, pathpatch_kw)

    return facetgrid
