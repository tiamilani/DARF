# © 2025 Nokia
# Licensed under the BSD 3-Clause License
# SPDX-License-Identifier: BSD-3-Clause
#
# Contact: Mattia Milani (Nokia) <mattia.milani@nokia.com>

"""
Configuration module
====================

Use this module to manage a configuration object.
"""

import configparser
import copy
from typing import Any, Union, Self

from darf.src.io.directories import DirectoryHandler as DH
from darf.src.io.files import FileHandler as FH


class ConfHandler:
    """ConfHandler.

	General object Configuration handler
    It uses the module configparser to manage and update the
    current configuration.
    """

    def __init__(self, conf_file: Union[FH, DH]):
        """__init__.

        Parameters
        ----------
        conf_file : FH
            conf_file where to find the configuration that
            needs to be loaded, the FH type is mandatory

        Raises
        ------
        TypeError
            If the FH type is not respected
        """
        self.cfg = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
        if isinstance(conf_file, FH):
            self.file = conf_file
            self.cfg.read(self.file.path)
        elif isinstance(conf_file, DH):
            self.file = conf_file.files
            self.cfg.read(self.file)
        else:
            raise TypeError(f"Conf file expected FileHandler or DirectoryHandler, \
                    obtained {type(conf_file)}")

    def update(self, conf: Union[FH, DH],
               inplace: bool = True) -> Union[None, Self]:
        """update.
        Is possible to update the current configuration
        with the content of the conf FH passed.
        The parameters inside the conf will have priority
        over the previous configuration.
        The FH `self.file` does not reflect the new FH.
        Is possible to obtain a new ConfHandler without
        performing this operation in place

        Parameters
        ----------
        conf : FH
            conf the new configuration file handler
        inplace : bool
            inplace, when active the change is done inplace
            otherwise a new copy is returned

        Returns
        -------
        Union[None, ConfHandler]

        """
        if inplace:
            if isinstance(conf, FH):
                self.cfg.read(conf.path)
            elif isinstance(conf, DH):
                self.cfg.read(conf.files)
            else:
                raise TypeError(f"Conf file expected FileHandler or DirectoryHandler, \
                        obtained {type(conf)}")
            return None
        new_cfg_h = copy.deepcopy(self)
        new_cfg_h.update(conf)
        return new_cfg_h

    def __getitem__(self, item: str) -> Any:
        """__getitem__.
        Get one item from the `self.cfg` object
        without calling the cfg attribute.

        Parameters
        ----------
        item : str
            item to retrieve

        Returns
        -------
        Any

        """
        # check if any object inside cfg[item] contains a \n and remove it
        for key in self.cfg[item]:
            self.cfg[item][key] = self.cfg[item][key].replace("\n", "")
        return self.cfg[item]
