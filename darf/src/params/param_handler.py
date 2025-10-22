# © 2025 Nokia
# Licensed under the BSD 3-Clause License
# SPDX-License-Identifier: BSD-3-Clause
#
# Contact: Mattia Milani (Nokia) <mattia.milani@nokia.com>

"""
paramHandler Module
===================

Primary entry point for managing parameters
"""

from typing import Any, Dict, List, Optional, Tuple, Union, Self

import re
import ast
import copy
import numpy as np
from darf.src.decorators import c_logger

from darf.src.util.strings import s
from darf.src.log import LogHandler as LH
from darf.src.io import IOHandler as IOH
from darf.src.io.configuration import ConfHandler as CH
from darf.src.util import compute_hash

from .param_wrapper import param_selector


@c_logger
class ParamHandler:
    """ParamHandler.
    Class used to handle and control parameters objects like datasets and
    plotters, it's used to evaluate the paths and the objects in the
    configuration file

    Each parameter could contain references to other objects items
    """

    def __init__(self, objects: List[Dict[str, str]],
                 ioh: IOH):
        """__init__.

        Parameters
        ----------
        objects : List[Dict[str, str]]
            objects
        ioh : IOH
            ioh
        """
        self.ioh = ioh
        self.objects = {}
        for obj in objects:
            self.objects[obj[s.io_name_key]] = self.define_object(obj)

        self.write_msg("ParamHandler class initialized", level=LH.DEBUG)
        self._force_hash = None

    @classmethod
    def apply_filter(cls, ph: Self, in_filter: str) -> Self:
        """apply_filter.

        Parameters
        ----------
        ph : ParamHandler
            ph
        filter : str
            filter

        Returns
        -------
        ParamHandler

        """
        keys = ph.filter_keys(in_filter)
        new_ph = copy.deepcopy(ph)
        new_ph.objects = {k: new_ph.get_handler(k) for k in new_ph.objects.keys() & keys}
        return new_ph

    @classmethod
    def get_param_sorting_order(cls, items: List[Dict[str, str]], io: IOH) -> List[int]:
        """get_param_sorting_order.

        Parameters
        ----------
        items : List[Dict[str, str]]
            items
        io : IOH
            io

        Returns
        -------
        List[int]

        """
        itms_names = np.array([x[s.io_name_key] for x in items])
        itms_names = np.append(itms_names, list(io.objects.keys()))
        itms_str = np.array(['-'.join([x[s.param_value],
                                       x.get(s.param_action_args, ""),
                                       x.get(s.param_action_kwargs, "")])
                             for x in items])
        itms_str = np.append(itms_str, ["-"]*len(list(io.objects.keys())))
        assert len(itms_names) == len(itms_str)
        itms_order = np.array([np.inf]*len(itms_str))
        # itms_to_solve = np.array([x.count('{') for x in itms_str])
        itms_str = np.array([re.sub(r"\\\{", r"\#", x) for x in itms_str])
        itms_str = np.array([re.sub(r"\\\}", r"\$", x) for x in itms_str])
        itms_objects = np.array([np.array(re.findall(r"\{[^\}]*\}", x))
                                for x in itms_str], dtype=object)
        itms_objects = np.array([np.array([x.replace('{', '').replace('}', '')
                                           for x in y]) for y in itms_objects],
                                dtype=object)
        itms_to_solve = np.array([len(x) for x in itms_objects])
        itms_order[itms_to_solve == 0] = 0
        changes = True
        counter = 0
        while changes:
            changes = False
            subset_idx = np.where(itms_order <= counter)[0]
            current_subset = itms_names[subset_idx]
            still_to_solve_idx = np.where(itms_order == np.inf)[0]
            still_to_solve = itms_objects[still_to_solve_idx]
            solved_idx = still_to_solve_idx[np.where(np.array([all(np.in1d(x, current_subset))
                                                               for x in still_to_solve]))[0]]
            if len(solved_idx) > 0:
                changes = True
            if len(solved_idx) == 0 and len(still_to_solve_idx) > 0:
                print(still_to_solve)
                print("csv_path" in itms_names)
                raise ValueError(f"Was not possible to solve some names: {still_to_solve}")

            itms_order[solved_idx] = counter+1
            counter += 1
        itms_order[itms_order == np.inf] = counter+1
        return itms_order

    @classmethod
    def from_cfg(cls, conf: CH, *args, **kwargs) -> Self:
        """from_cfg.

        Parameters
        ----------
        conf : CH
            conf
        args :
            args
        kwargs :
            kwargs

        Returns
        -------
        ParamHandler

        """
        items = []
        other_items = []
        for key in conf.cfg.keys():
            if len(conf.cfg.items(key)) > 0:
                d = dict(conf.cfg.items(key))
                d[s.io_name_key] = key
                if d[s.io_type_key] in s.param_types:
                    items.append(d)
                elif d[s.io_type_key] not in s.io_types:
                    other_items.append(d)
        order = cls.get_param_sorting_order(items, args[0])
        for d, o in zip(items, order):
            d["Order"] = o
        items = sorted(items, key=lambda x: x["Order"])
        for d in items:
            del d["Order"]
        items.extend(other_items)
        return cls(items, *args, **kwargs)

    def __get_args(self, obj: Dict[str, str]) -> Tuple:
        """__get_args.

        Local function that evaluates if the args attribute is in the
        object and return the value.
        If the attribute is not present return an empty tuple
        If the attribute is present and it's a string return the parsed value
        If the attribute is present and it's not a string it must be a Tuple
        and return the value.
        Otherwise the function raises an Exception

        Parameters
        ----------
        obj : Dict[str, str]
            obj

        Returns
        -------
        Tuple
            The parse args value

        Raises
        ------
        ValueError
            If the attribute is not a string or a Tuple
        """
        if s.param_action_args in obj.keys() and obj[s.param_action_args] is not None:
            if isinstance(obj[s.param_action_args], str):
                self.write_msg(f"{obj[s.param_value]} Has an args list")
                coma = ""
                if ',' not in obj[s.param_action_args]:
                    coma=","
                args_to_eval = f"({self.evaluate(obj[s.param_action_args])}{coma})"
                obj[s.param_action_args] = ast.literal_eval(args_to_eval)
                return obj[s.param_action_args]
            if isinstance(obj[s.param_action_args], tuple):
                return obj[s.param_action_args]
            raise ValueError("args must be a string or a tuple, not" \
                             f"{type(obj[s.param_action_args])}")
        return ()

    def __get_kwargs(self, obj: Dict[str, str]) -> Dict:
        """__get_kwargs.

        Local function that evaluates if the kwargs attribute is in the
        object and return the value.
        If the attribute is not present return an empty dict
        If the attribute is present and it's a string return the parsed value
        If the attribute is present and it's not a string it must be a Dict
        and return the value.
        Otherwise the function raises an Exception

        Parameters
        ----------
        obj : Dict[str, str]
            obj

        Returns
        -------
        Dict
            The parse kwargs value

        Raises
        ------
        ValueError
            If the attribute is not a string or a Dict
        """
        if s.param_action_kwargs in obj.keys() and obj[s.param_action_kwargs] is not None:
            if isinstance(obj[s.param_action_kwargs], str):
                self.write_msg(f"{obj[s.param_value]} Has a kwargs list")
                kwargs_to_eval = f"{{{self.evaluate(obj[s.param_action_kwargs])}}}"
                return ast.literal_eval(kwargs_to_eval)
            if isinstance(obj[s.param_action_kwargs], dict):
                return obj[s.param_action_kwargs]
            raise ValueError("kwargs must be a string or a dict, not"\
                             f"{type(obj[s.param_action_kwargs])}")
        return {}

    def define_object(self, obj: Dict[str, str]):
        """define_object.

        Parameters
        ----------
        """
        self.write_msg(f"Evaluation of {obj[s.param_value]}", level=LH.DEBUG)
        obj[s.param_value] = self.evaluate(obj[s.param_value])
        if obj[s.io_type_key] in s.param_args_ast:
            self.write_msg(f"{obj[s.param_value]} is in the args list")

            obj[s.param_action_args] = self.__get_args(obj)
            obj[s.param_action_kwargs] = self.__get_kwargs(obj)

        self.write_msg(f"After evaluation: {obj[s.param_value]}", level=LH.DEBUG)
        return param_selector(obj[s.io_type_key], obj, logger=self.logger)

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
            self.write_msg(f"{obj} is contained in the self objects", level=LH.DEBUG)
            return obj, self.objects[obj].value
        self.write_msg(f"{obj} is not contained in the self objects, asking the IOH",
                       level=LH.DEBUG)
        return obj, self.ioh.evaluate_obj(obj)[1]

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

    def evaluate(self, pth: str) -> str:
        """evaluate.
        Evaluate a path if it contains other objects in it

        Parameters
        ----------
        pth : str
            pth

        Returns
        -------
        str

        """
        self.write_msg(f"Evaluating {pth}", level=LH.DEBUG)
        pth = re.sub(r"\\\{", r"\#", pth)
        pth = re.sub(r"\\\}", r"\$", pth)
        result = re.findall(r"\{[^\}]*\}", pth)
        res = {x[0]: x[1] for x in self.evaluate_objs(result)}
        pth = pth.replace('!', '').format(**res)
        pth = pth.replace(r"\#", "{")
        pth = pth.replace(r"\$", "}")
        self.write_msg(f"After the evaluation: {pth}", level=LH.DEBUG)
        return pth

    def get(self, elem: str, literal_eval: bool = False) -> Union[str, Any]:
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
        self.write_msg(f"Required the value for object: {elem}", level=LH.DEBUG)
        if elem not in self.objects:
            raise ValueError(f"Available objects: {self.objects.keys()}, {elem} not found")
        return self.objects[elem].value if not literal_eval \
                else ast.literal_eval(self.objects[elem].value)

    def get_handler(self, elem: str) -> Any:
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
        self.write_msg(f"Required the handler for object: {elem}", level=LH.DEBUG)
        if elem not in self.objects:
            raise ValueError(f"Available objects: {self.objects.keys()}, {elem} not found")
        return self.objects[elem]


    def __getitem__(self, item: Union[str, Tuple[str, bool]]) -> Union[str, Any]:
        """__getitem__.

        Parameters
        ----------
        item : str
            item that should be returned

        Returns
        -------
        str

        """
        if isinstance(item, str):
            item = (item, False)
        assert len(item) == 2 and isinstance(item[0], str) and isinstance(item[1], bool)
        return self.get(item[0], literal_eval=item[1])

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

    def filter_keys(self, in_type: str) -> List[str]:
        """filter_keys.

        Parameters
        ----------
        in_type : str
            type

        Returns
        -------
        List[str]

        """
        res = []
        self.write_msg(f"Filter keys on {type} type", level=LH.DEBUG)
        for elem in self.objects.values():
            if elem.type == in_type:
                res.append(elem.name)
        self.write_msg(f"Elements found: {len(res)}", level=LH.DEBUG)
        return res

    def filter_handler(self, in_type: str) -> List[str]:
        """filter_handler.

        Parameters
        ----------
        type : str
            type

        Returns
        -------
        List[str]

        """
        res = []
        self.write_msg(f"Filter handler on {in_type} type", level=LH.DEBUG)
        for elem in self.objects.values():
            if elem.type == in_type:
                res.append(elem)
        self.write_msg(f"Elements found: {len(res)}", level=LH.DEBUG)
        return res

    def __str__(self) -> str:
        """__str__.
        Return all the objects in string format

        Returns
        -------
        str

        """
        res = "All Parameters:\n"
        for key, val in self.objects.items():
            res += f"{key}: {val}\n"
        return res

    @property
    def force_hash(self) -> Optional[str]:
        """force_hash.

        Parameters
        ----------

        Returns
        -------
        Optional[str]

        """
        if self._force_hash is None:
            self._force_hash = compute_hash(str(self), digest_size=8)
        return self._force_hash

    @force_hash.setter
    def force_hash(self, in_hash: str) -> None:
        """force_hash.

        Parameters
        ----------
        in_hash : str
            hash to be setted

        Returns
        -------
        None

        """
        self._force_hash = in_hash
