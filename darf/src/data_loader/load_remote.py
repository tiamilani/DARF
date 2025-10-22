# © 2025 Nokia
# Licensed under the BSD 3-Clause License
# SPDX-License-Identifier: BSD-3-Clause
#
# Contact: Mattia Milani (Nokia) <mattia.milani@nokia.com>

"""
loadRemote module
=================

Use this module to manage a Remote loader.
"""

from typing import Optional

import pandas as pd

from darf.src.decorators import data_loader
from darf.src.data_loader import Base
from darf.src.io.remote import RemoteHandler as RH

@data_loader
class Remote(Base):
    """Remote.
	"""

    def sanity_check(self) -> bool:
        return True


    def __call__(self, *args, local: Optional[str] = None,
                 **kwargs) -> pd.DataFrame:
        rh = RH(self.value, local_path=local)
        local_file = rh.transfer_file()
        self.data = pd.read_csv(local_file)
        return self.data
