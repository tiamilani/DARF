# © 2025 Nokia
# Licensed under the BSD 3-Clause License
# SPDX-License-Identifier: BSD-3-Clause
#
# Contact: Mattia Milani (Nokia) <mattia.milani@nokia.com>

"""
Pickle handler module
=====================

Use this module to manage pickle objects.
It permits to load and save pickle objects.
It must be initialized with the variables required to create uniquePickleFiles.

"""

import os
import pickle as pkl

from typing import Any, Optional

from darf.src.util.strings import s
from darf.src.decorators import c_logger
from darf.src.log import LogHandler as LH

from .io_handler import IOHandler as IOH

@c_logger
class PickleHandler: # pylint: disable=unexpected-keyword-arg
    """PickleHandler.

    General Pickle object handler class
    """

    def __init__(self, io_handler: IOH,
                 apendix: str,
                 in_hash: str = ""):
        """__init__.

        Parameters
        ----------
        IoH : IOH
            Input output object from which the output pkl path is obtained
        apendix : str
            Apendix to the experiment output files
        in_hash : str
            Hash to append to the experiment id
        """
        self.output_folder: str = io_handler[s.pkl_path]
        self.apendix: str = apendix
        self.hash: str = in_hash
        self.write_msg("Pickle handler initialized")

    def __filepath(self, name: str,
                   override: bool = False,
                   custom_hash: Optional[str] = None,
                   disable_unique_id: bool = False) -> str:
        """__filepath.
        Function to generate the path to a pkl file given the name of the file
        without the extension

        Parameters
        ----------
        name : str
            name
        override : bool
            Used to flag that the filepath function should not modify the
            passed value.
        custom_hash : str
            custom hash to append to the file name
        disable_unique_id : bool
            disable the unique id, the filepath will be returned
            as 'name.pkl' instead of 'name_unique_id.pkl'

        Returns
        -------
        str

        """
        if override:
            return name

        file_name = f"{name}_{self.apendix}_{self.hash}.pkl"
        if custom_hash is not None:
            file_name = f"{name}_{self.apendix}_{custom_hash}.pkl"
        if disable_unique_id:
            file_name = f"{name}.pkl"
        return os.path.join(self.output_folder, file_name)

    def save(self, sv_object: object, name: str,
             override: bool = False, **kwargs) -> None:
        """save.
        Function used to save an object to a file with the given name

        Parameters
        ----------
        sv_object : object
            object that needs to be saved
        name : str
            name of the file to write
        override :
            override if true then the file will be overwritten otherwise
            an exception will be throw
        kwargs :
            additional arguments passed to the filepath function
            is possible to pass a custom hash or disable the
            uniq id.

        Returns
        -------
        None

        """
        file_path = self.__filepath(name, **kwargs)
        self.write_msg(f"Saving a pickle object at the following path: {file_path}", LH.DEBUG)

        if not override and os.path.exists(file_path):
            self.write_msg(f"{file_path} already exists, override option disabled", LH.ERROR)
            raise FileExistsError(f"{file_path} Already exists, pickle creation abortion")

        with open(file_path, 'wb') as file:
            pkl.dump(sv_object, file)

        self.write_msg(f"{file_path} written")

    def load(self, name: str, **kwargs) -> Any:
        """load.
        Given a name load the corresponding object and returns it

        Parameters
        ----------
        name : str
            name
        kwargs :
            additional arguments passed to the filepath function
            is possible to pass a custom hash or disable the
            uniq id.

        Returns
        -------
        object

        """
        file_path = self.__filepath(name, **kwargs)
        self.write_msg(f"Loading a pickle object from the following path: {file_path}", LH.DEBUG)

        if not os.path.exists(file_path):
            self.write_msg(f"{file_path} does not exists impossible loading", LH.ERROR)
            raise FileNotFoundError(f"{file_path} Not found, pickle loading aboarted")

        with open(file_path, 'rb') as file:
            self.write_msg(f"{file_path} Loaded")
            return pkl.load(file)

    def check(self, name: str, **kwargs) -> bool:
        """check.
        Check if a given name corresponds to an existsing pickle file

        Parameters
        ----------
        name : str
            name
        kwargs :
            additional arguments passed to the filepath function
            is possible to pass a custom hash or disable the
            uniq id.

        Returns
        -------
        bool
            if the pikle exists or not

        """
        file_path = self.__filepath(name, **kwargs)
        return os.path.exists(file_path)
