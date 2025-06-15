# © 2025 Nokia
# Licensed under the BSD 3-Clause License
# SPDX-License-Identifier: BSD-3-Clause
#
# Contact: Mattia Milani (Nokia) <mattia.milani@nokia.com>

"""
Load Local
==========

This module is used to load a locally available dataset.
The dataset is loaded expecting a ``.csv`` file provided as a path.

This module is used when the ``origin=Local`` keyword is used in the configuration file.

An example of configuration file that loads a local available csv file is the following
configuration:

.. code-block:: ini

    [test_dataset]
    type=dataset
    origin=Local
    value=<path to a local csv file>

The correct loading of the dataset can be tested using the following command:

.. code-block:: bash

    darf -c conf.ini -D test_dataset

"""

import pandas as pd

from darf.src.decorators import data_loader
from darf.src.data_loader import Base
from darf.src.io.files import FileHandler as FH

@data_loader
class Local(Base):
    """Local.

    Load a local type object and apply transformations on it
    There might be multiple types of local datasets to load
    each differnt type can be processed in different ways depending on
    the requirements.
    But the final results would always be a pandas dataframe with the raw
    information inside of it.

    Is out of the scope of this class to then apply operations on top of the
    loaded pkl dataframe. This is the responsibility of the user of this class.

    This function keeps an object that represent the loaded object
    remember to remvoe from memory the object if a copy has been made.
	"""

    def sanity_check(self) -> bool:
        """sanity_check.

        Method to check if the self.__value is in the correct form.
        self.__value is expected to be a file path.
        The file must exists otherwise throw an error

        Returns
        -------
        bool
            True if self.__value is a file path and the file exists
        """
        return FH.exists(self.value)


    def __call__(self) -> pd.DataFrame:
        """__call__.

        Load the local CSV file as pd dataframe and return it, save also the
        result in self.data
        """
        self.data = pd.read_csv(self.value)
        return self.data
