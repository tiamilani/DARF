# © 2025 Nokia
# Licensed under the BSD 3-Clause License
# SPDX-License-Identifier: BSD-3-Clause
#
# Contact: Mattia Milani (Nokia) <mattia.milani@nokia.com>

"""
plotter module
==============

Use this module to create beautiful plots

"""


from typing import List, Callable, Optional, Any

import pandas as pd
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import patches
from matplotlib import ticker
from matplotlib.lines import Line2D

from darf.src.decorators import plot_functions

class Plotter: # pylint: disable=unused-variable
    """Plotter.
    Class to plot single dataframe statistics
    """

    # pylint: disable=too-many-arguments, too-many-positional-arguments
    def __init__(self, data: pd.DataFrame,
                 show: bool = False,
                 out_format: Optional[List[str]] = None,
                 font_scale: float = 1.5,
                 palette=None):
        """__init__.

        Parameters
        ----------
        data : pd.DataFrame
            dataframe that should be plotted
        show : bool
            show flag
        """
        self.__properties = {
                    "df": data,
                    "show": show,
                    "format": out_format if out_format is not None else ["pdf"],
                    "font_scale": font_scale,
                    "font": "times",
                    "palette": palette
                }
        self.plot = None
        self.other_plots = None

        # Seaborn settings
        self.sns_reset()

    def __call__(self, f_name, *args, **kwargs):
        """__call__.

        Parameters
        ----------
        f_name :
            f_name
        args :
            args
        kwargs :
            kwargs
        """
        if f_name in plot_functions:
            # Do not pass default palette if it has already been defined
            # in kwargs
            if "palette" not in kwargs:
                kwargs["palette"] = self.palette

            self.plot = plot_functions[f_name](*args, data=self.df, **kwargs)
            if isinstance(self.plot, list) and \
                    len(self.plot) == 2:
                self.other_plots = self.plot[1:]
                self.plot = self.plot[0]
        else:
            raise ValueError(f"{f_name} Not found in the plot functions available")

    def apply(self, operation: Callable) -> None:
        """apply.

        Parameters
        ----------
        operation : Callable
            operation

        Returns
        -------
        None

        """
        self.plot = operation(self.df, self.plot)

    def save(self, output_file: str,
             **kwargs) -> None:
        """save.

        Parameters
        ----------
        output_file : str
            output_file
        kwargs :
            kwargs

        Returns
        -------
        None

        """
        if isinstance(self.plot, list):
            for i, plt_obj in enumerate(self.plot):
                for fmt in self.out_format:
                    output_file_i = f"{output_file.split('.')[0]}_{i}.{fmt}"
                    plt_obj.savefig(output_file_i, format=fmt, bbox_inches="tight", **kwargs)
            plt.close()
        else:
            for fmt in self.out_format:
                output_file = f"{output_file.split('.')[0]}.{fmt}"
                plt.savefig(output_file, format=fmt, bbox_inches="tight", **kwargs)
            plt.close()

    def set_legend(self, x: float = 0.5,
                   y: float = -0.32,
                   loc: str = "lower center",
                   ncol: int = 3,
                   borderaxespad: int = 0,
                   **kwargs) -> None:
        """set_legend.

        Parameters
        ----------
        x : float
            x
        y : float
            y
        loc : str
            loc
        ncol : int
            ncol
        borderaxespad : int
            borderaxespad
        kwargs :
            kwargs

        Returns
        -------
        None

        """
        self.plot.axes.legend(bbox_to_anchor=(x, y),
                              loc=loc,
                              ncol=ncol,
                              borderaxespad=borderaxespad,
                              **kwargs)

    def move_legend(self, *args, obj: Optional[Any] = None, **kwargs):
        """move_legend.

        Parameters
        ----------
        args :
            args
        obj : Optional[Any]
            obj
        kwargs :
            kwargs
        """
        if obj is None:
            obj = self.plot
        sns.move_legend(obj, *args, **kwargs)

    def sns_set(self, *args, **kwargs) -> None:
        """sns_set.

        Parameters
        ----------
        args :
            args
        kwargs :
            kwargs

        Returns
        -------
        None

        """
        sns.set(*args, **kwargs)

    def sns_set_api(self, *args, interface: Callable = sns.set, **kwargs) -> None:
        """sns_set_api.

        Parameters
        ----------
        interface : Callable
            interface
        args :
            args
        kwargs :
            kwargs

        Returns
        -------
        None

        """
        interface(*args, **kwargs)

    def sns_reset(self) -> None:
        """sns_reset.

        Parameters
        ----------

        Returns
        -------
        None

        """
        self.sns_set_api(font_scale=self.font_scale)
        self.sns_set_api("white", interface=sns.set_style)
        self.sns_set_api(sns.color_palette(), interface=sns.set_palette)
        plt.rcParams.update({
            "font.family": "sans-serif",
            "ps.usedistiller": 'xpdf',
            "font.size": 16,
        })

    def set_special(self, keyword: str, *args, **kwargs) -> None:
        """set_special.

        Parameters
        ----------
        keyword : str
            keyword
        args :
            args
        kwargs :
            kwargs

        Returns
        -------
        None

        """
        match keyword:
            case "xrotate":
                self.plot.tick_params(**kwargs)
            case "xticks":
                self.plot.set_xticks(*args, **kwargs)
            case "yticks":
                self.plot.set_yticks(*args, **kwargs)
            case "ygrid":
                self.plot.yaxis.grid(*args, **kwargs)
            case "joint-title":
                if isinstance(self.plot, list):
                    for i, p in enumerate(self.plot):
                        title = kwargs.get("title", None)
                        title += f" Iter. {i}" if title is not None else f" Iter. {i}"
                        p.fig.suptitle(title)
            case _:
                raise ValueError(f"Keyword {keyword} not recognized")

    def difficult_joint_scatter(self) -> None:
        """difficult_joint_scatter.

        Parameters
        ----------

        Returns
        -------
        None

        """
        ax = plt.gca()
        self.plot.figure.set_layout_engine('constrained')
        b_patch = patches.Patch(color=self.palette[0], label=r"$\widetilde{G}$")
        g_patch = patches.Patch(color=self.palette[1], label=r"$\widetilde{B}$")
        point_b = Line2D([0], [0], label=r"$\widetilde{D}$", marker='o', markersize=10,
        markeredgecolor="black", markerfacecolor="black", linestyle='')
        ax.legend(handles=[g_patch, b_patch, point_b], ncol=1, loc="lower left",
                  bbox_to_anchor=(-0.55, 0.15))
        # ax = plt.gca()
        # ax.legend().remove()
        # self.plot.figure.set_layout_engine('constrained')
        # cax = self.other_plots[0].inset_axes([1.05, 0.05, 0.05, 0.95])
        # cmap = sns.cubehelix_palette(start=.5, rot=-.75, as_cmap=True, reverse=True)
        # self.plot.figure.colorbar(mpl.cm.ScalarMappable(norm=mpl.colors.Normalize(0.5, 10),
        #                                 cmap=cmap), cax=cax,
        #                           orientation='vertical', ticks=[1.0, 5.0, 9.0],
        #                           format=ticker.FixedFormatter(['9', '5', '1']),
        #                           fraction=0.05, pad=0.5,
        #                           label=r"$\widetilde{D}$ \#Outage minutes")

    def inference_emb_joint_scatter(self) -> None:
        """inference_emb_joint_scatter.

        Parameters
        ----------

        Returns
        -------
        None

        """
        ax = plt.gca()
        self.plot.figure.set_layout_engine('constrained')
        b_patch = patches.Patch(color=self.palette[0], label=r"$\hat{G}$")
        g_patch = patches.Patch(color=self.palette[1], label=r"$\hat{B}$")
        point_b = Line2D([0], [0], label="Sep.", marker='o', markersize=10,
        markeredgecolor="black", markerfacecolor="black", linestyle='')
        ax.legend(handles=[g_patch, b_patch, point_b], ncol=3, loc="lower left",
                  title="Classes")
        cax = self.other_plots[0].inset_axes([1.22, 0.05, 0.05, 0.95])
        cmap = sns.cubehelix_palette(start=.5, rot=-.75, as_cmap=True)
        self.plot.figure.colorbar(mpl.cm.ScalarMappable(norm=mpl.colors.Normalize(0, 1),
                                        cmap=cmap), cax=cax,
                                  orientation='vertical', ticks=[0.01, 0.25, 0.5, 0.75, 0.99],
                                  format=ticker.FixedFormatter(['1%', '25%', '50%', '75%', '99%']),
                                  fraction=0.05, pad=0.5,
                                  label="Outage prob.")

    def inference_emb_joint_scatter_dst_legend(self) -> None:
        """inference_emb_joint_scatter.

        Parameters
        ----------

        Returns
        -------
        None

        """
        ax = plt.gca()
        self.plot.figure.set_layout_engine('constrained')
        b_patch = patches.Patch(color=self.palette[0], label=r"$\hat{G}$")
        g_patch = patches.Patch(color=self.palette[1], label=r"$\hat{B}$")
        point_b = Line2D([0], [0], label="Sep.", marker='o', markersize=10,
        markeredgecolor="black", markerfacecolor="black", linestyle='')
        ax.legend(handles=[g_patch, b_patch, point_b], ncol=3, loc="upper center",
                  title="Classes", bbox_to_anchor=(0.5, -0.2))
        # cax = self.other_plots[0].inset_axes([1.22, 0.05, 0.05, 0.95])
        # cmap = sns.cubehelix_palette(start=.5, rot=-.75, as_cmap=True)
        # self.plot.figure.colorbar(mpl.cm.ScalarMappable(norm=mpl.colors.Normalize(1.4, 3.6),
        #                                 cmap=cmap), cax=cax,
        #                           orientation='vertical', ticks=[1.5, 2.0, 2.5, 3.0, 3.5],
        #                           format=ticker.FixedFormatter(['1.5', '2.0', '2.5', '3.0', '3.5']),
        #                           fraction=0.10, pad=0.5,
        #                           label="AP+AN")


    def emb_joint_legend(self) -> None:
        """emb_joint_legend.

        Parameters
        ----------

        Returns
        -------
        None

        """
        ax = plt.gca()
        self.plot.figure.set_layout_engine('constrained')
        b_patch = patches.Patch(color=self.palette[0], label=r"$\hat{G}$")
        g_patch = patches.Patch(color=self.palette[1], label=r"$\hat{B}$")
        ax.legend(handles=[g_patch, b_patch], loc="lower left",
                    title="Classes")

    def emb_joint_legend_sequence(self) -> None:
        """emb_joint_legend_sequence.

        Parameters
        ----------

        Returns
        -------
        None

        """
        for p in self.plot:
            ax = p.ax_joint
            p.figure.set_layout_engine('constrained')
            b_patch = patches.Patch(color=self.palette[0], label=r"$\hat{G}$")
            g_patch = patches.Patch(color=self.palette[1], label=r"$\hat{B}$")
            point_d = Line2D([0], [0], label=r"$\hat{D}$", marker='o', markersize=10,
                             markeredgecolor="black", markerfacecolor="black", linestyle='')
            point_rep_g = Line2D([0], [0], label=r"$Rep_{\hat{G}}$", marker='o', markersize=10,
                                markeredgecolor="red", markerfacecolor="red", linestyle='')
            point_rep_b = Line2D([0], [0], label=r"$Rep_{\hat{B}}$", marker='o', markersize=10,
                                markeredgecolor="yellow", markerfacecolor="yellow", linestyle='')
            ax.legend(handles=[g_patch, b_patch, point_d, point_rep_g, point_rep_b],
                      loc="lower center",
                      bbox_to_anchor=(0.5, -0.45),
                      title="Classes", ncol=3)

    def special_legend(self, keyword: str, *args, **kwargs) -> None: # pylint: disable=unused-argument
        """special_legend.

        Parameters
        ----------
        keyword : str
            keyword
        args :
            args
        kwargs :
            kwargs

        Returns
        -------
        None

        """
        match keyword:
            case "difficult_joint_scatter":
                self.difficult_joint_scatter()
            case "emb_joint_sequence":
                self.emb_joint_legend_sequence()
            case "emb_joint":
                self.emb_joint_legend()
            case "inference_emb_joint_scatter":
                self.inference_emb_joint_scatter()
            case "inference_emb_joint_scatter_dst_legend":
                self.inference_emb_joint_scatter_dst_legend()
            case _:
                raise ValueError(f"Keyword {keyword} not recognized")

    def set(self, *args, **kwargs) -> None:
        """set.

        Parameters
        ----------
        args :
            args
        kwargs :
            kwargs

        Returns
        -------
        None

        """
        if self.plot is not None:
            self.plot.set(*args, **kwargs)
        else:
            raise ValueError("A plot must be first created")

    @property
    def df(self) -> pd.DataFrame:
        """df.

        Parameters
        ----------

        Returns
        -------
        pd.DataFrame

        """
        return self.__properties["df"]

    @property
    def show(self) -> bool:
        """show.

        Parameters
        ----------

        Returns
        -------
        bool

        """
        return self.__properties["show"]

    @property
    def out_format(self) -> List[str]:
        """format.

        Parameters
        ----------

        Returns
        -------
        List[str]

        """
        return self.__properties["format"]

    @property
    def font_scale(self) -> float:
        """font_scale.

        Parameters
        ----------

        Returns
        -------
        float

        """
        return self.__properties["font_scale"]

    @property
    def font(self) -> str:
        """font.

        Parameters
        ----------

        Returns
        -------
        str

        """
        return self.__properties["font"]

    @property
    def palette(self):
        """palette.
        """
        return self.__properties["palette"]
