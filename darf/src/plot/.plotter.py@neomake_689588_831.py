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
# Copyright (C) 2020 Mattia Milani <mattia.milani.ext@nokia.com>

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

from seacoral.src.decorators import plot_functions

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
            self.plot = plot_functions[f_name](*args, data=self.df, **kwargs,
                                               palette=self.palette)
            if isinstance(self.plot, list) and \
                    len(self.plot) == 2:
                self.other_plots = self.plot[1:]
                self.plot = self.plot[0]
        else:
            raise ValueError(f"{f_name} Not found in the plot functions available")

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
        b_patch = patches.Patch(color=self.palette[0], label=r"$\hat{G}$")
        g_patch = patches.Patch(color=self.palette[1], label=r"$\hat{B}$")
        point_b = Line2D([0], [0], label=r"$\hat{D}$", marker='o', markersize=10,
        markeredgecolor="black", markerfacecolor="black", linestyle='')
        ax.legend(handles=[g_patch, b_patch, point_b], ncol=3, loc="lower left",
                  title="Classes")
        # img = self.other_plots[0].imshow(None)
        # cax = self.other_plots[0].inset_axes([1.22, 0.05, 0.05, 0.95])
        # cmap = sns.cubehelix_palette(start=.5, rot=-.75, as_cmap=True, reverse=True)
        # self.plot.figure.colorbar(mpl.cm.ScalarMappable(norm=mpl.colors.Normalize(1, 10),
        #                                 cmap=cmap), cax=cax,
        #                           orientation='vertical', ticks=[1.1, 9.9],
        #                           format=ticker.FixedFormatter(['Low', 'High']),
        #                           fraction=0.05, pad=0.5,
        #                           label=r"$\hat{D}$ Difficulty level")

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
