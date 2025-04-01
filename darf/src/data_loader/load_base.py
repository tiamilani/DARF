# © 2025 Nokia
# Licensed under the BSD 3-Clause License
# SPDX-License-Identifier: BSD-3-Clause
#
# Contact: Mattia Milani (Nokia) <mattia.milani@nokia.com>

"""
Loader module
=============

Use this module to abstract the loader class complexity.
"""

import pandas as pd

from darf.src.decorators import c_logger

@c_logger
class Base:
    """Base.

    Class used as a baseline for all the data_loaders.

    The call method for this class would raise an exception.

    Provides all the basic objects that data loaders should use, like
    an __init__ method that checks if the path passed exists and
    sanity checks for the other functions.
    Plus the correct deletion of the objects.
    """

    def __init__(self, value: str, *args, **kwargs): # pylint: disable=unused-argument
        """__init__.

        Parameters
        ----------
        path : str
            Path to the file to load
        """
        self.__value = value
        self.__data = None
        self.write_msg(f"Loading from {self.__value}")

        self.sanity_check()

    def sanity_check(self) -> bool:
        """sanity_check.

        Method to check if the self.__value is in the correct form.
        This function always returns True in the base class.

        Returns
        -------
        bool
            Always True
        """
        return True

    def __del__(self):
        """__del__.
        Destructor method
        """
        if self.__data is not None:
            del self.__data

    def __call__(self) -> pd.DataFrame:
        """__call__.
        Call method for the class

        Raises
        ------
        NotImplementedError
            If the method is called

        Returns
        -------
        pd.DataFrame
            The data loaded
        """
        raise NotImplementedError("This method should be implemented in the child classes")

    def __str__(self) -> str:
        """__str__.
        String representation of the class

        Returns
        -------
        str
            The string representation of the class
        """
        return f"Data loader for {self.__value}"

    @property
    def value(self) -> str:
        """value.

        Returns
        -------
        str
            The value of the class
        """
        return self.__value


    @value.setter
    def value(self, value: str) -> None:
        """value.

        Parameters
        ----------
        value : str
            The value to set
        """
        self.__value = value

    @property
    def data(self) -> pd.DataFrame:
        """data.

        Returns
        -------
        pd.DataFrame
            The data loaded
        """
        return self.__data

    @data.setter
    def data(self, data: pd.DataFrame) -> None:
        """data.

        Parameters
        ----------
        data : pd.DataFrame
            The data to set
        """
        self.__data = data
