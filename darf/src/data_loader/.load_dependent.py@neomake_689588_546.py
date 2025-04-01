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
# Copyright (C) 2024 Mattia Milani <mattia.milani@nokia.com>

"""
loadDependent module
====================

Use this module to manage a loader that depends on other datasets
"""

import pandas as pd

from seacoral.src.decorators import data_loader, data_loaders
from seacoral.src.data_loader import Base

@data_loader
class Dependent(Base):
    """Dependent.

    Load a dependent type object and apply transformations on it
    There might be multiple different Dependent flows, check which one is more
    suitable for your use case.
    But the final results would always be a pandas dataframe with the raw
    information inside of it.

    Is out of the scope of this class to then apply operations on top of the
    loaded dataframe. This is the responsibility of the user of this class.

    The default behaviour is to concatenate the list of dependant datasets
    passed, the axis of the concat could be passed to the __call__ method.
	"""

    def sanity_check(self) -> bool:
        """sanity_check.

        Method to check if the self.__value is in the correct form.
        self.__value is expected to be a dictionary in form of {key: pd.DataFrame}
        the DFs must be not empty otherwise throw an error

        Returns
        -------
        bool
            True if self.__value is a dictionary of non null dataframes
        """
        if not isinstance(self.value, dict):
            raise ValueError(f"Expected a dictionary got {type(self.value)}")
        for _, value in self.value.items():
            if not isinstance(value, pd.DataFrame):
                raise ValueError(f"Expected a dictionary of pd.DataFrame got {type(value)}")
            if value.empty:
                raise ValueError(f"Expected a dictionary of non empty pd.DataFrame got {value}")
        return True


    def __call__(self, *args, **kwargs) -> pd.DataFrame:
        """__call__.

        Merge the list of dependent datasets and return it.
        This method uses the pd.concat method, passing the args and kwargs
        received asis.

        the main argument of pd.concat is the list of dataframes to merge
        obtained from the dictionary in self.value

        Parameters
        ----------
        args : tuple
            list of args to pass to pd.concat
        kwargs : dict
            dictionary of arguments to pass to pd.concat

        Returns
        -------
        pd.DataFrame
            the merged dataframe
        """
        dfs = [df.reset_index(drop=True) for df in self.value.values()]
        self.data = pd.concat(dfs, *args, **kwargs)
        return self.data

@data_loader
class Join(Base):

    def sanity_check(self) -> bool:
        """sanity_check.

        Method to check if the self.__value is in the correct form.
        self.__value is expected to be a dictionary in form of {key: pd.DataFrame}
        the DFs must be not empty otherwise throw an error

        Returns
        -------
        bool
            True if self.__value is a dictionary of non null dataframes
        """
        if not isinstance(self.value, dict):
            raise ValueError(f"Expected a dictionary got {type(self.value)}")
        for _, value in self.value.items():
            if not isinstance(value, pd.DataFrame):
                raise ValueError(f"Expected a dictionary of pd.DataFrame got {type(value)}")
            if value.empty:
                raise ValueError(f"Expected a dictionary of non empty pd.DataFrame got {value}")
        if len(self.value.values()) != 2:
            raise ValueError(f"Expected a dictionary with two elements got {len(self.value)}")
        return True


    def __call__(self, *args, **kwargs) -> pd.DataFrame:
        # check if the on parameter is in kwargs
        df1 = list(self.value.values())[0]
        df2 = list(self.value.values())[1]
        if 'on' in kwargs:
            on_param = kwargs.pop('on')
            unique_on_df2 
        else:
            self.data = df1.join(df2, *args, **kwargs)
        return self.data

@data_loader
class Copy(data_loaders['Dependent']):
    """Copy.

    Special case of the Dependent loader.
    This loader requires that the dictionary of values contains only one
    object and it will return a copy of the object instead of a merge of it.
	"""

    def sanity_check(self) -> bool:
        """sanity_check.

        Requires the Dependent sanity check, but also checks that the dictionary
        contains only one object

        Returns
        -------
        bool
            True if self.__value is a dictionary with one non null dataframe
        """
        super().sanity_check()
        if len(self.value) != 1:
            raise ValueError(f"Expected a dictionary with one element got {len(self.value)}")
        return True


    def __call__(self, *args, **kwargs) -> pd.DataFrame:
        """__call__.

        Return a copy of the only object in the dictionary

        Parameters
        ----------
        args : tuple
            list of args to pass to pd.concat
        kwargs : dict
            dictionary of arguments to pass to pd.concat

        Returns
        -------
        pd.DataFrame
            the merged dataframe
        """
        # Prblem when specifying subclassing through a list
        self.data = self.value[list(self.value.keys())[0]].copy() # pylint: disable=attribute-defined-outside-init
        return self.data
