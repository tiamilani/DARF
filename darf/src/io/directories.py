# © 2025 Nokia
# Licensed under the BSD 3-Clause License
# SPDX-License-Identifier: BSD-3-Clause
#
# Contact: Mattia Milani (Nokia) <mattia.milani@nokia.com>

"""
Directory module
================

Use this module to handle directories

"""

import os
from pathlib import Path
import shutil

from typing import List

class DirectoryHandler:
    """DirectoryHandler.
    Class used to manage directories
    """


    def __init__(self, path: str, create: bool = True):
        """__init__.
        if the directory passed doesn't exists and create is
        false then an exception is generated

        Parameters
        ----------
        path : str
            path to the directory position
        create : bool
            create the directory if it doesn't exists

        Raises
        ------
        FileNotFoundError
        """
        self.__path = path
        if not os.path.exists(self.__path):
            if create:
                os.makedirs(self.__path)
            else:
                raise FileNotFoundError(f"{self.__path} not Found")

    @property
    def path(self) -> str:
        """path of the directory managed

        Parameters
        ----------

        Returns
        -------
        str
            the path to the directory

        """
        return self.__path

    @property
    def files(self) -> List[str]:
        """Returns the list of files in the directory controlled.
        This would search recoursivly for files.

        Parameters
        ----------

        Returns
        -------
        List[str]

        """
        return list(Path(self.path).rglob("*"))

    @classmethod
    def clear(cls, path: str) -> None:
        """clear.
        Function to clear the directory
        Removes all the files and directories in the path.
        recusively!
        Use with caution.

        Parameters
        ----------
        path : str
            path

        Returns
        -------
        None

        """
        for elem in os.scandir(path):
            try:
                if os.path.isfile(elem) or os.path.islink(elem):
                    os.unlink(elem)
                elif os.path.isdir(elem):
                    shutil.rmtree(elem)
            except OSError as exception:
                print(f"Failed to delete {elem}. Reason: {exception}")
                raise exception

    @classmethod
    def check(cls, path: str) -> bool:
        """check.
        Function to check if the path provided is
        a directory

        Parameters
        ----------
        path : str
            path

        Returns
        -------
        bool
            True if the directory exists

        """
        return os.path.isdir(path)

    def __str__(self) -> str:
        """__str__.

        Parameters
        ----------

        Returns
        -------
        str

        """
        return f"Directory Handler: {self.path}"
