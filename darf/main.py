# © 2025 Nokia
# Licensed under the BSD 3-Clause License
# SPDX-License-Identifier: BSD-3-Clause
#
# Contact: Mattia Milani (Nokia) <mattia.milani@nokia.com>

"""
Main module
===========

Main module of the project, use it to load all the different parts and
generate the required datasets plots.

"""
import argparse
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import pkg_resources

from darf.src.environment.conf import conf as env_conf
from darf.src.util.strings import s
from darf.src.io import DirectoryHandler as DH
from darf.src.io import FileHandler as FH
from darf.src.io import ConfHandler as CH
from darf.src.io import IOHandler as IOH
from darf.src.log import LogHandler as LH
from darf.src.params import ParamHandler as PH
from darf.src.io import PickleHandler as PkH
from darf.src import DatasetManager as Data
from darf.src.plot import PlotManager as PM


parser = argparse.ArgumentParser(usage="usage: main.py [options]",
                      description="Execute plots from configurations",
                      formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-c", "--conf", dest="conf", default="Conf/default",
                    action="store", help="define the input configuration it can be a single \
                            ini file or a folder containing multiples")
parser.add_argument("-v", "--verbose", dest="verbosity", default=1,
                    action="count", help=s.verbose_help)
parser.add_argument("-D", "--show-data", nargs='*', dest="show_data", default=None,
                    action="store", help="Enable the visualization of the datasets \
                            on STDOUT, if no argument is provided the full list of \
                            datasets is printed, otehrwise only the provided \
                            datasets are printed")
parser.add_argument("-H", "--hash", dest="fix_hash", default=None,
                    action="store", help="Define a fixed hash")
parser.add_argument("--force-data", dest="force_data", default=False,
                    action="store_true", help="Force the regeneration of all the datasets")
parser.add_argument("--force-plot", dest="force_plot", default=False,
                    action="store_true", help="Force the regeneration of all the plots")

def main():
    """main.
    Main function of the project
    """
    # Parse the arguments
    options = parser.parse_args()

    # Load the custom configuration files
    if DH.check(options.conf):
        custom_conf: DH = DH(options.conf, create=False)
    else:
        custom_conf: FH = FH(options.conf, create=False)

    # check that the default configuration exists
    assert pkg_resources.resource_exists(__name__, s.default_conf)
    default_conf = pkg_resources.resource_filename(__name__, s.default_conf)
    conf: CH = CH(DH(default_conf))
    conf.update(custom_conf)

    io: IOH = IOH.from_cfg(conf)
    logger: LH = LH(io[s.log_file], LH.find_ll(options.verbosity))

    logger("darf.main", "Loading the parameters")
    pm = PH.from_cfg(conf, io, logger=logger)
    if options.fix_hash is not None:
        pm.force_hash = options.fix_hash

    pkh = PkH(io, pm[s.appendix_key],
              in_hash=pm.force_hash,
              logger=logger)

    logger("darf.main", "Environment configuration")
    env_conf(PH.apply_filter(pm, s.env_par), logger=logger)

    logger("darf.main", "load datasets")
    data = Data.from_cfg(PH.apply_filter(pm, s.dataset_obj_type),
                         operations=PH.apply_filter(pm, s.param_op_type),
                         force=options.force_data,
                         pklh=pkh, logger=logger)

    if options.show_data is not None:
        data.show(options.show_data)

    logger("darf.main", "Execute plots")
    plot_man = PM(PH.apply_filter(pm, s.param_plot_type),
                  PH.apply_filter(pm, s.param_plot_op_type),
                  data, io, force=options.force_plot, logger=logger)
    plot_man.execute()

if __name__ == "__main__":
    main()
