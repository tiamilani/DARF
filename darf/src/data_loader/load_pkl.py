# © 2025 Nokia
# Licensed under the BSD 3-Clause License
# SPDX-License-Identifier: BSD-3-Clause
#
# Contact: Mattia Milani (Nokia) <mattia.milani@nokia.com>

"""
LoadPklt module
===============

Use this module to manage a pkl loader.
"""

from typing import List

import re
import numpy as np
import pandas as pd
import tensorflow as tf
tf.get_logger().setLevel('ERROR')
tf.autograph.set_verbosity(1)

from darf.src.io import PickleHandler as PkH
from darf.src.io import FileHandler as FH
from darf.src.decorators import data_loader, data_loaders
from darf.src.data_loader import Base
from darf.src.io.remote import RemoteHandler as RH

@data_loader
class CsvPkl(Base):
    """CsvPkl.

    Load a Csv file that has been pkled.

    Is out of the scope of this class to then apply operations on top of the
    loaded pkl dataframe. This is the responsibility of the user of this class.

    This function keeps an object that represent the loaded pkl object
    remember to remvoe from memory the object if a copy has been made.
    """

    def __init__(self, *args, pklh: PkH = None, **kwargs):
        """__init__.
        """
        self.__pklh = pklh
        super().__init__(*args, **kwargs)
        self.write_msg(f"Loading Pkl with args {args} and kwargs {kwargs}") # pylint: disable=no-member

    def sanity_check(self) -> bool:
        """sanity_check.

        Method to check if the self.__value is in the correct form.
        self.__value is expected to be a loadable pkl file.
        The file must exists otherwise throw an error
        Check using self.__pklh.check function

        Returns
        -------
        bool
            True if self.__value is a file path and the file exists to a pkl
        """
        return self.__pklh.check(self.value, override=True)

    def __call__(self, *args, **kwargs) -> pd.DataFrame:
        """__call__.
        """
        self.data = self.__pklh.load(self.value, override=True)
        return self.data

    @property
    def pklh(self) -> PkH:
        """pklh.
        """
        return self.__pklh

@data_loader
class TfPkl(Base):
    """TfPkl.

    Load a pkl type object and apply transformations on it
    There might be multiple types of pkl datasets to load
    each differnt type can be processed in different ways depending on
    the requirements.
    But the final results would always be a pandas dataframe with the raw
    information inside of it.

    Is out of the scope of this class to then apply operations on top of the
    loaded pkl dataframe. This is the responsibility of the user of this class.

    This function keeps an object that represent the loaded pkl object
    remember to remvoe from memory the object if a copy has been made.
    """

    def __init__(self, *args, pklh: PkH = None, **kwargs):
        """__init__.
        """
        self.__pklh = pklh
        super().__init__(*args, **kwargs)
        self.write_msg(f"Loading Pkl with args {args} and kwargs {kwargs}") # pylint: disable=no-member

    def sanity_check(self) -> bool:
        """sanity_check.

        Method to check if the self.__value is in the correct form.
        self.__value is expected to be a loadable pkl file.
        The file must exists otherwise throw an error
        Check using self.__pklh.check function

        Returns
        -------
        bool
            True if self.__value is a file path and the file exists to a pkl
        """
        return self.__pklh.check(self.value, override=True)

    def tfl2df(self, obj: List[tf.Tensor]) -> pd.DataFrame:
        """tfl2df.

        Method to convert a list of tf.Tensor objects into a pandas dataframe

        Parameters
        ----------
        obj : list[tf.Tensor]
            list of tf.Tensor objects

        Returns
        -------
        pd.DataFrame
            pandas dataframe with the values of the tf.Tensor objects
        """
        obj = tf.concat(obj, axis=0)
        obj = pd.DataFrame(obj.numpy())
        return obj

    def __call__(self, *args, **kwargs) -> pd.DataFrame:
        """__call__.
        """
        obj = self.__pklh.load(self.value, override=True)
        self.data = self.tfl2df(obj)
        return self.data

    @property
    def pklh(self) -> PkH:
        """pklh.
        """
        return self.__pklh

# pylint: disable=attribute-defined-outside-init
@data_loader
class TfPklList(data_loaders['TfPkl']):
    """TfPklList.

    Class used to load a list of TfPkl.
    The output is still a single DF but for each file the 'Label' column
    is incremented by 1, starting from 0.
    Transofrms each file into a pandas dataframe and then concatenate them
    """

    def sanity_check(self) -> bool:
        """sanity_check.

        Method to check if the self.__value is in the correct form.
        self.__value is expected to be a list of loadable pkl file.
        All file must exists otherwise throw an error
        Check using self.__pklh.check function

        Returns
        -------
        bool
            True if self.__value is a list of file path and all file exists to a pkl
        """
        # use a generator to check all files
        return all(self.pklh.check(o, override=True) for o in self.value)

    def __call__(self, *args, **kwargs) -> pd.DataFrame:
        """__call__.
        """

        # Load locally remote files present in the list and replace the path in the list
        for f in self.value:
            # Identify if f contains a remote path (presence of : in the path)
            if re.search(r":", f):
                rh = RH(f, local_path=kwargs.get('local', None))
                local_file = rh.transfer_file()
                self.value[self.value.index(f)] = local_file

        objs = [self.pklh.load(o, override=True) for o in self.value]
        dfs = [self.tfl2df(o) for o in objs]
        for i, df in enumerate(dfs):
            df['Label'] = i
        self.data = pd.concat(dfs, axis=0)
        self.data['Label'] = self.data['Label'].astype('U13')
        return self.data

# pylint: disable=attribute-defined-outside-init
@data_loader
class ObjPklList(data_loaders['TfPklList']):
    """ObjPklList.
    Classe used to manage pkld objects that can be converted back
    into a pandas dataframe.
    """

    def __call__(self, *args, **kwargs) -> pd.DataFrame:
        """__call__.
        """
        # Load locally remote files present in the list and replace the path in the list
        for f in self.value:
            # Identify if f contains a remote path (presence of : in the path)
            if re.search(r":", f):
                rh = RH(f, local_path=kwargs.get('local', None))
                local_file = rh.transfer_file()
                self.value[self.value.index(f)] = local_file

        objs = [self.pklh.load(o, override=True) for o in self.value]
        if len(objs[0] > 5000):
            objs[0] = objs[0][:5000]

        dfs = [self.tfl2df(o) for o in objs]
        self.data = pd.concat(dfs, axis=0)
        self.data = self.data.apply(pd.to_numeric)
        return self.data

# pylint: disable=attribute-defined-outside-init
@data_loader
class TfPklListIterator(data_loaders['TfPkl']):
    """TfPklListIterator.

    This class takes as input a pklList where there is a wildcard
    inside the paths.
    This means that the wildcard represents an incremental number of
    iterations.
    This difference should also be visible in the dataset, including an
    iteration column.
    """

    def __init__(self, *args,
                 start: int = 0,
                 end: int = -1,
                 **kwargs):
        """__init__.

        Parameters
        ----------
        start : int
            Start of the iteration cycles to consider
        end : int
            End of the iteration cycles to consider
        """
        self.__start = start
        self.__end = end
        super().__init__(*args, **kwargs)
        self.write_msg(f"Loading Pkl with args {args} and kwargs {kwargs}")

    def sanity_check(self) -> bool:
        """sanity_check.

        Method to check if the self.__value is in the correct form.
        self.__value is expected to be a list of loadable pkl files with
        a wildcard.
        All file must exists otherwise throw an error
        Check using self.__pklh.check function

        Returns
        -------
        bool
            True if self.__value is a list of file path and all file exists to a pkl
        """
        return all(FH.exists(o, use_glob=True) for o in self.value)
        # return all([self.pklh.check(o, override=True) for o in self.value])

    def __call__(self, *args,
                 label_regex: str = r".*",
                 iter_regex: str = r".*",
                 label_clm: str = "Label",
                 label_iter_clm: str = "Iteration",
                 **kwargs) -> pd.DataFrame:
        """__call__.
        """

        # For each file in values get the full list of files
        files = np.array([FH.get_wildcard(o) for o in self.value])

        # For each file in the list get the corresponding label using the
        # regex pattern
        def lookup(x, l):
            return re.search(l, x).group(0)
        labels = np.vectorize(lookup)(files, label_regex)
        iter_ids = np.vectorize(lookup)(files, iter_regex)
        iter_ids = iter_ids.astype(np.int8)

        # Use self.__start and seld.__end to subselect the arrays
        if self.__end == -1:
            self.__end = np.max(iter_ids)

        mask = (iter_ids >= self.__start) & (iter_ids <= self.__end)
        iter_ids, labels, files = iter_ids[mask], labels[mask], files[mask]

        # Get the DFs from the files
        def get_df(f, l, i):
            obj = self.pklh.load(f, override=True)
            df = self.tfl2df(obj)
            df[label_clm] = l
            df[label_iter_clm] = i
            return df
        dfs = np.vectorize(get_df)(files, labels, iter_ids)
        self.data = pd.concat(dfs, axis=0)
        self.data = self.data.apply(pd.to_numeric, errors="ignore", downcast="float")

        return self.data
