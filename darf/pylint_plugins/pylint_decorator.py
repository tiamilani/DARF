# © 2025 Nokia
# Licensed under the BSD 3-Clause License
# SPDX-License-Identifier: BSD-3-Clause
#
# Contact: Mattia Milani (Nokia) <mattia.milani@nokia.com>

"""
Pylint_Decorator module
=======================

This is a custom plugin for pylint that will add the capability to
understand and contextualize decorators that modifies classes members and
attributes inside the project
"""

# Inside hello_plugin.py
# from typing import TYPE_CHECKING
#
# import astroid
#
# if TYPE_CHECKING:
#     from pylint.lint import PyLinter
#
#
# def register(linter: "PyLinter") -> None:
#   """This required method auto registers the checker during initialization.
#
#   :param linter: The linter to register the checker to.
#   """
#   print('Hello world')

import astroid
from astroid import MANAGER

def register(linter): # pylint: disable=unused-argument, unused-variable
    """register.

    Parameters
    ----------
    linter :
        linter
    """
    # Needed for registering the plugin.
    MANAGER.register_transform(astroid.ClassDef, transform)

def transform(cls):
    """transform.

    Parameters
    ----------
    cls :
        cls
    """
    if not cls.decorators: return
    # print(cls.decorators.nodes)
    # for node in cls.decorators.nodes:
    #     print(getattr(node, 'name', None))
    extension_module = None
    classes = ['c_logger']
    if any(map(lambda x: getattr(x, 'name', None) in classes, cls.decorators.nodes)):
        extension_module = astroid.parse("""
def write_msg(self, *args, **kwargs):
    pass
self.logger = None
""")
    if not extension_module is None:
        for name, objs in extension_module.locals.items():
            # print(name)
            # print(objs)
            # print(cls.locals)
            cls.locals[name] = objs
            # print(cls.locals[name])
