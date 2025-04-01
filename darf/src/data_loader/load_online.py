# © 2025 Nokia
# Licensed under the BSD 3-Clause License
# SPDX-License-Identifier: BSD-3-Clause
#
# Contact: Mattia Milani (Nokia) <mattia.milani@nokia.com>

"""
Load Online module
==================

Use this module to manage an Online loader.
"""

import pandas as pd
import seaborn as sns

from darf.src.decorators import data_loader
from darf.src.data_loader  import Base

@data_loader
class Online(Base):
    """LoadPkl.

    Load an online type object and apply transformations on it
    But the final results would always be a pandas dataframe with the raw
    information inside of it.

    Is out of the scope of this class to then apply operations on top of the
    loaded pkl dataframe. This is the responsibility of the user of this class.

    This function keeps an object that represent the loaded object
    remember to remvoe from memory the object if a copy has been made.
	"""

    def __call__(self, *args, **kwargs) -> pd.DataFrame:
        """__call__.

        Load the local CSV file as pd dataframe and return it, save also the
        result in self.data

        Parameters
        ----------
        args :
            args, Not used
        kwargs :
            kwargs, Not used

        Returns
        -------
        pd.DataFrame
            The loaded dataframe
        """
        self.data = sns.load_dataset(self.value)
        return self.data
