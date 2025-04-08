# © 2025 Nokia
# Licensed under the BSD 3-Clause License
# SPDX-License-Identifier: BSD-3-Clause
#
# Contact: Mattia Milani (Nokia) <mattia.milani@nokia.com>

"""
IO Module
=========

Use this module to control io objects from the configuration file

"""

from typing import List, TypeVar, Union, Tuple, Self
import re
import pkg_resources

from darf.src.util.strings import s
from .files import FileHandler as fh
from .directories import DirectoryHandler as dh
from .remote import RemoteHandler as rh
from .configuration import ConfHandler as CH
from .command_interpolation import fn as cm_interpolation


T = TypeVar('T')

class IOHandler:
    """IOHandler.
    Class used to handle and control io objects like file and folders
    """


    def __init__(self, in_object: List[dict]):
        """__init__.

        Parameters
        ----------
        object : List[dict]
            Dictionary list of objects that must be handled
        """
        self.objects = {}
        for obj in in_object:
            self.objects[obj[s.io_name_key]] = self.define_object(obj)

    @classmethod
    def from_cfg(cls, conf: CH) -> Self:
        """from_cfg.
        Read an IO configuration from a configuration handler object

        Parameters
        ----------
        conf : CH
            conf

        Returns
        -------
        IOHandler

        """
        items = []
        for key in conf.cfg.keys():
            if len(conf.cfg.items(key)) == 0:
                continue

            d = dict(conf.cfg.items(key))

            if d[s.io_type_key] not in s.io_types:
                continue

            d[s.io_name_key] = key
            d[s.io_exists_key] = True if s.io_exists_key not in d else \
                                    conf.cfg.getboolean(key, s.io_exists_key)

            if d[s.io_path_key] == "__name__":
                d[s.io_path_key] = pkg_resources.resource_filename("darf.main", "")

            items.append(d)
        return cls(items)

    def define_object(self, obj: dict) -> dh | fh:
        """define_object.
        Function used to define a single object and associate it to the
        DirectoryHandler or the FileHandler

        Parameters
        ----------
        obj : dict
            Single object that must be handled
        """
        path = self.evaluate_path(obj[s.io_path_key])
        create = not obj[s.io_exists_key]
        local_path = None
        _type = obj[s.io_type_key]

        match _type:
            case x if x in s.folder_obj_types:
                return dh(path, create=create)
            case x if x in s.file_obj_types:
                return fh(path, create=create)
            case x if x in s.remote_obj_types:
                if s.local_path_key in obj:
                    local_path = self.evaluate_path(obj[s.local_path_key])
                return rh(path, local_path=local_path)
            case _:
                raise ValueError(f"object {obj[s.io_name_key]} type {_type} not handled")

    def evaluate_obj(self, obj: str) -> Tuple[str, str]:
        """evaluate_obj.

        Parameters
        ----------
        obj : str
            obj

        Returns
        -------
        Tuple[str, str]

        """
        obj = obj.replace('{', '').replace('}', '')
        if obj in self.objects:
            return obj, self.get(obj)
        return obj[1::], cm_interpolation(obj)

    def evaluate_objs(self, objs: List[str]) -> List[Tuple[str, str]]:
        """evaluate_objs.

        Parameters
        ----------
        objs : List[str]
            objs

        Returns
        -------
        List[Tuple[str, str]]

        """
        return [self.evaluate_obj(obj) for obj in objs]

    def evaluate_path(self, pth: str) -> str:
        """evaluate_path.
        Evaluate a path if it contains other objects in it

        Parameters
        ----------
        pth : str
            pth

        Returns
        -------
        str

        """
        result = re.findall(r"\{[^\}]*\}", pth)
        res = {x[0]: x[1] for x in self.evaluate_objs(result)}
        pth = pth.replace('!', '').format(**res)
        return pth

    def get(self, elem: T) -> str:
        """get.
        Returns the path of an object

        Parameters
        ----------
        elem : str
            elem

        Returns
        -------
        str

        """
        return self.objects[elem].path

    def get_handler(self, elem: str) -> Union[fh, dh]:
        """get.
        Returns the handler of an object

        Parameters
        ----------
        elem : str
            elem

        Returns
        -------
        str

        """
        return self.objects[elem]


    def __getitem__(self, item: str) -> str:
        """__getitem__.

        Parameters
        ----------
        item : str
            item that should be returned

        Returns
        -------
        str

        """
        return self.get(item)

    def check(self, key: str) -> bool:
        """check.

        Parameters
        ----------
        key : str
            key

        Returns
        -------
        bool

        """
        return key in self.objects

    def __str__(self) -> str:
        """__str__.
        Return an object in string format

        Returns
        -------
        str

        """

        res = "All IoH:\n"
        for key, val in self.objects.items():
            res += f"{key}: {val}\n"
        return res
