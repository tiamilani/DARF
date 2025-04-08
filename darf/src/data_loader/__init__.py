"""
Load Module
===========

Module used to load data from different sources
"""

from .load_base import Base
from .load_local import Local
from .load_online import Online
from .load_pkl import *
from .load_dependent import Dependent, Copy, Join
from .load_remote import Remote
