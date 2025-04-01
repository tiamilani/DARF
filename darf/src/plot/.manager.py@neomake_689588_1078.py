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
# Copyright (C) 2024 Mattia Milani <mattia.milani.ext@nokia.com>

"""
plotter manager module
======================

Use this module to create and manage plotter objects

"""

from typing import Self

from seacoral.src.params import ParamHandler as PH
from seacoral.src import DatasetManager as DM
from seacoral.src.io import FileHandler as FH
from seacoral.src.io import IOHandler as IOH
from seacoral.src.io import Pb as pb
from seacoral.src.plot.plotter import Plotter
from seacoral.src.decorators import c_logger
from seacoral.src.util.strings import s


@c_logger
class PlotManager:
    """PlotManager.

    Class used to manage plotter objects, it accepts a configuration object
    as input, and it will automaticall generate the plotter objects necessary.
    Will also manage the correct configuration of io and data objects.
    """

    def __init__(self, cfg: PH, operations: PH,
                 data: DM, io: IOH,
                 force: bool = False) -> Self:
        """__init__.

        Parameters
        ----------
        cfg : PH
            configuration object
        data : DM
            data object

        Returns
        -------
        plotter
        """
        self.cfg = cfg
        self.plot_operations = operations
        self.data = data
        self.io = io
        self.plotters = {}
        self.force = force

        self.plotters_init()

    def plotters_init(self) -> None:
        """plotters_init.
        Initialize the plotter objects with the configurations passed.

        Parameters
        ----------

        Returns
        -------
        None

        """
        pbar = pb.tq_bar(total=len(self.cfg.objects.keys()),
                      ascii=True, desc="Loading plots ...",
                      bar_format="{desc} {n_fmt}/{total_fmt} [{elapsed}]")
        for plt_key in self.cfg.objects.keys():
            plt_obj = self.cfg.objects[plt_key]

            self.plotters[plt_key] = Plotter(self.data[plt_obj.dataset], show=False,
                                             out_format=plt_obj.extensions,
                                             palette=plt_obj.palete)
            pbar.update(1)

        pbar.close()

    def execute(self) -> None:
        """execute.
        Execute the plot generation

        Parameters
        ----------

        Returns
        -------
        None

        """
        pbar = pb.tq_bar(total=len(self.cfg.objects.keys()),
                      ascii=True, desc="Plot generation ...",
                      bar_format="{desc} {n_fmt}/{total_fmt} [{elapsed}]")
        for key, plot in self.plotters.items():
            pbar.set_description_str(f"Plot generation {key}")

            plot_keywords = self.cfg.objects[key]

            if not self.force and not plot_keywords.regenerate and \
                    FH.exists(f"{self.io[s.results_path]}/{plot_keywords.output_name}.*",
                              use_glob=True):
                pbar.update(1)
                continue

            plot_operations = plot_keywords.operations
            raise Exception

            plot(plot_keywords.value, *plot_keywords.args, **plot_keywords.kwargs)

            if plot_keywords.set_kwargs is not None:
                plot.set(**plot_keywords.set_kwargs)

            if len(plot_keywords.set_special.keys()) > 0:
                for k, v in plot_keywords.set_special.items():
                    plot.set_special(k, *v[0], **(v[1]))

            if plot_keywords.legend_flag:
                if plot_keywords.special_legend is not None:
                    plot.special_legend(plot_keywords.special_legend)
                else:
                    plot.set_legend(**plot_keywords.set_legend)

            plot.save(f"{self.io[s.results_path]}/{plot_keywords.output_name}")

            pbar.update(1)

        pbar.set_description_str("Plot generation compleated")
        pbar.close()
