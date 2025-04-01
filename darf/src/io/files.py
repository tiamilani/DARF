# © 2025 Nokia
# Licensed under the BSD 3-Clause License
# SPDX-License-Identifier: BSD-3-Clause
#
# Contact: Mattia Milani (Nokia) <mattia.milani@nokia.com>

"""
files module
============

Use this module to handle files

"""

from typing import List, Optional, Self

import os
import glob

from darf.src.io.directories import DirectoryHandler as DH


class FileHandler:
    """FileHandler.
    Class to manage single files
    """


    def __init__(self, filepath: str,
                 create: bool = True):
        """__init__.
        If the file passed doesn't exists it will be
        created, respecting the flag create.
        If the flag is false and the file doesn't
        exists an exception will be raised

        Parameters
        ----------
        filepath : str
            path to the file to use
        create : bool
            If it is possible it will create the file, if it doesn't exists

        Raises
        -----
        FileNotFoundError if create False and the file doesn't exists
        """

        self.__filename: str = filepath.split("/")[-1]
        self.__path: str = os.path.join("/".join(filepath.split("/")[:-1]))
        self.__filepath: str = filepath
        # Check if the path exists
        if not os.path.exists(self.__filepath):
            if create:
                os.mknod(self.__filepath)
            else:
                raise FileNotFoundError(f"{self.__filepath}")

    def __str__(self) -> str:
        """__str__.
        print information about the file handler

        Parameters
        ----------

        Returns
        -------
        str

        """
        return f"File handler: {self.path}"

    @property
    def path(self) -> str:
        """path.

        Parameters
        ----------

        Returns
        -------
        str
            the complete file path to the destination file

        """
        return self.__filepath

    @property
    def folder_path(self) -> str:
        """folder_path.
        Get the folder path of a file

        Parameters
        ----------

        Returns
        -------
        str the path to the file, without the file, only the folders

        """
        return self.__path

    def get(self, extension: str) -> str:
        """get.
        Permits to get a file path with the same file name as the handled one
        plus an appendix, remember the type of the file, the part after the '.'
        will be removed

        Parameters
        ----------
        extension : str
            string to use instead of the default desinence of the file

        Returns
        -------
        str the filepath modified

        """
        pth = self.__filepath.split(".")[0]
        pth += f".{extension}"
        return pth

    @staticmethod
    def exists(filepath: str,
               use_glob: bool = False) -> bool:
        """exists.
        Return if a file exists or not

        Parameters
        ----------
        filepath : str
            filepath
        use_glob : bool
            if true the file will be searched using glob instead of os.path.exists

        Returns
        -------
        bool

        """
        if use_glob:
            return len(glob.glob(filepath)) > 0
        return os.path.exists(filepath)

    @staticmethod
    def get_wildcard(filepath: str) -> List[str]:
        """get_wildcard.
        Get the list of files that match the 'filepath' considering
        a possible wildcard

        Parameters
        ----------
        filepath : str
            filepath

        Returns
        -------
        List[str]
            List of the files that match the wildcard
        """
        return glob.glob(filepath)

    @classmethod
    def detect(cls, in_dir: DH) -> List[Self]:
        """detect.
        Get the list of files in a directory as FileHandlers

        Parameters
        ----------
        dir : DH
            dir

        Returns
        -------
        List[FileHandler]

        """
        return [cls(file) for file in in_dir.files]

    @staticmethod
    def hash_path(path: str, in_hash: Optional[str] = None) -> str:
        """hash_path.
        Get the path with the hash appended

        Parameters
        ----------
        path : str
            path
        in_hash : Optional[str]
            hash given as input

        Returns
        -------
        str

        """
        if hash is None:
            return path
        lpath = path.split('.')
        return f"{lpath[0]}-{in_hash}.{lpath[1]}"

    @property
    def filename(self) -> str:
        """filename.

        Parameters
        ----------

        Returns
        -------
        str
            the name of the file

        """
        return self.__filename


    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        return self

    def __eq__(self, other):
        return self.path == other.path

    def __ne__(self, other):
        return not self == other
