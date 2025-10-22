# © 2025 Nokia
# Licensed under the BSD 3-Clause License
# SPDX-License-Identifier: BSD-3-Clause
#
# Contact: Mattia Milani (Nokia) <mattia.milani@nokia.com>

"""
loadList module
===============

Use this module to manage a loader that manages a list of datasets
"""

from typing import List

import pandas as pd

from darf.src.decorators import data_loader
from darf.src.data_loader import Base
from darf.src.io.directories import DirectoryHandler as DH
from darf.src.io.files import FileHandler as FH

@data_loader
class CsvList(Base):
    """CsvList.

    Load a List type object and apply transformations on it
    There might be multiple different flows, check which one is more
    suitable for your use case.
    But the final results would always be a List of pandas dataframes with the
    raw information inside of it.

    Is out of the scope of this class to then apply operations on top of the
    loaded dataframes. This is the responsibility of the user of this class.

    The default behaviour is to return the list of datasets loaded,
	"""

    def sanity_check(self) -> bool:
        """sanity_check.

        Method to check if the self.__value is in the correct form.
        self.__value is expected to be a single string value, which
        containst the path to the folder/regex to load the datasets

        Returns
        -------
        bool
            True if self.__value is a string to a folder and or contains
            a regex to load the datasets.

        Raises
        ------
        ValueError
            If the value is not a string in the correct format
        """
        if not isinstance(self.value, dict):
            raise ValueError(f"Expected a dictionary got {type(self.value)}")
        for _, value in self.value.items():
            if not isinstance(value, pd.DataFrame):
                raise ValueError(f"Expected a dictionary of pd.DataFrame got {type(value)}")
            if value.empty:
                raise ValueError(f"Expected a dictionary of non empty pd.DataFrame got {value}")
        return True


    def __call__(self, path: str, *args, **kwargs) -> List[pd.DataFrame]:
        """__call__.

        Generate the lsit of dataframes pointed by `self.__value` and returns it.

        The path should be passed as a single argument.

        No kweyword arguments are expected.
        Kwargs kept for possible subclassing.

        Parameters
        ----------
        path : str
            path to the folder or regex to load the datasets
        args : tuple
            list of args to pass to pd.concat
        kwargs : dict
            dictionary of arguments to pass to pd.concat

        Returns
        -------
        List[pd.DataFrame]
            List of dataframes
        """
        # identify if the path is a folder or a regex
        # if it is a folder, load all the files in the folder
        # if it is a regex, load all the files that match the regex
        # return the list of dataframes

        files: List[str] = None
        if DH.check(path):
            files = DH(path).files
        else:
            files = FH.get_wildcard(path)

        print(files)

        dfs = [pd.read_csv(file) for file in files]
        print(dfs)

        raise NotImplementedError
