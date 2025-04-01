# © 2025 Nokia
# Licensed under the BSD 3-Clause License
# SPDX-License-Identifier: BSD-3-Clause
#
# Contact: Mattia Milani (Nokia) <mattia.milani@nokia.com>

"""
plotter manager module
======================

Use this module to create and manage plotter objects

"""

from typing import Self

from darf.src.params import ParamHandler as PH
from darf.src import DatasetManager as DM
from darf.src.io import FileHandler as FH
from darf.src.io import IOHandler as IOH
from darf.src.io import Pb as pb
from darf.src.plot.plotter import Plotter
from darf.src.decorators import c_logger
from darf.src.util.strings import s


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
        pbar = pb.tq_bar(len(self.cfg.objects.keys()), desc="Loading plots ...")
        for plt_key in self.cfg.objects.keys():
            plt_obj = self.cfg.objects[plt_key]

            if not self.force and not plt_obj.regenerate and \
                    FH.exists(f"{self.io[s.results_path]}/{plt_obj.output_name}.*",
                              use_glob=True):
                pbar.update(1)
                continue

            self.plotters[plt_key] = Plotter(self.data[plt_obj.dataset], show=False,
                                             out_format=plt_obj.extensions,
                                             palette=plt_obj.palete)
            pbar.update(1)

        pb.success_close(pbar, "Plots loaded")

    def execute(self) -> None:
        """execute.
        Execute the plot generation

        Parameters
        ----------

        Returns
        -------
        None

        """
        pbar = pb.tq_bar(len(self.plotters.keys()), desc="Plot generation ...")
        for key, plot in self.plotters.items():
            pbar.set_description_str(f"Plot generation {key}")

            plot_keywords = self.cfg.objects[key]

            if not self.force and not plot_keywords.regenerate and \
                    FH.exists(f"{self.io[s.results_path]}/{plot_keywords.output_name}.*",
                              use_glob=True):
                pbar.update(1)
                continue

            plot(plot_keywords.value, *plot_keywords.args, **plot_keywords.kwargs)

            for op in plot_keywords.operations:
                pbar.set_description_str(f"Plot generation {key} - applying {op}")
                plot.apply(self.plot_operations.get_handler(op))

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

        pb.success_close(pbar, "Plot generation compleated")
