# © 2025 Nokia
# Licensed under the BSD 3-Clause License
# SPDX-License-Identifier: BSD-3-Clause
#
# Contact: Mattia Milani (Nokia) <mattia.milani@nokia.com>

"""
class module
============

Use this module to manage all the parameters of a class.
"""

from typing import Dict, Any, Callable, Optional

import ast

from darf.src.util.strings import s
from darf.src.log import LogHandler as LH


class _param:
    """_param.
    """


    def none_log(self, *args, **kwargs):
        """none_log.

        Parameters
        ----------
        args :
            args
        kwargs :
            kwargs
        """

    def __init__(self, d: Dict[str, str],
                 logger: Optional[LH] = None):
        """__init__.

        Parameters
        ----------
        d : Dict[str, str]
            d
        logger : Optional[LH]
            logger
        """
        self.name = d[s.io_name_key]
        self.type = d[s.io_type_key]
        self.value = d[s.param_value]
        self.logger = logger
        if self.logger is None:
            self.logger = self.none_log
        self.logger(self.__class__.__name__, f"{self.name} - {self.type} -> {self.value} Loaded")

    def __str__(self):
        """__str__.
        """
        return f"Param {self.name}, type: {self.type}, value: {self.value}"

class TypeSpecific(_param):
    """TypeSpecific_param.
    """

    def __init__(self, d: Dict[str, str],
                 param_type: str = s.param_generic_type,
                 **kwargs):
        """__init__.

        Parameters
        ----------
        d : Dict[str, str]
            d
        param_type : str
            param_type
        kwargs :
            kwargs
        """
        if d[s.io_type_key] != param_type:
            raise ValueError(f"Required {param_type} type, given {d[s.io_type_key]}")
        super().__init__(d, **kwargs)

class Plot(TypeSpecific):
    """Plot.
    """

    def __init__(self, d: Dict[str, str],
                 param_type: str = s.param_generic_type,
                 **kwargs):
        """__init__.

        Parameters
        ----------
        d : Dict[str, str]
            d
        param_type : str
            param_type
        kwargs :
            kwargs
        """
        self.dataset=d[s.plot_datasets_key]

        self.extensions = ['pdf', 'png']
        if s.plot_extensions_key in d.keys():
            self.extensions=ast.literal_eval(d[s.plot_extensions_key])

        self.output_name="default"
        if s.plot_output_name_key in d.keys():
            self.output_name=d[s.plot_output_name_key]

        if s.plot_dataset_merge_axis_key in d.keys():
            raise ValueError("The merge axis is not available anymore, \
                    use the dataset dependencies")

        self.palete = None
        if s.plot_palette_key in d.keys():
            self.palete = ast.literal_eval(d[s.plot_palette_key])

        self.regenerate = False
        if s.plot_regenerate_key in d.keys():
            self.regenerate = ast.literal_eval(d[s.plot_regenerate_key])

        if s.plot_dataset_keywords_key in d.keys():
            raise ValueError("The dataset keywords are not available anymore, \
                    use the dataset dependencies")

        self.legend_flag = False
        if s.plot_legend_key in d.keys():
            self.legend_flag = ast.literal_eval(d[s.plot_legend_key])

        self.special_legend = None
        if s.plot_special_legend_key in d.keys():
            self.special_legend = d[s.plot_special_legend_key]

        self.args=d[s.param_action_args]
        # print()
        # if s.param_action_args in d.keys():
        #     self.args = ast.literal_eval(d[s.param_action_args])
        self.kwargs= d[s.param_action_kwargs]
        # if s.param_action_kwargs in d.keys():
        #     self.kwargs = ast.literal_eval(d[s.param_action_kwargs])

        self.set_kwargs = None
        if s.plot_set_kwargs_key in d.keys():
            self.set_kwargs = ast.literal_eval(d[s.plot_set_kwargs_key])
        self.set_special = {}
        if s.plot_set_special_key in d.keys():
            self.set_special = ast.literal_eval(d[s.plot_set_special_key])
        self.set_legend = {}
        if s.plot_set_legend_key in d.keys():
            self.set_legend = ast.literal_eval(d[s.plot_set_legend_key])

        self.operations = []
        if s.plot_operations_key in d.keys():
            self.operations = ast.literal_eval(d[s.plot_operations_key])
        super().__init__(d, param_type=s.param_plot_type, **kwargs)

class Dataset(TypeSpecific):
    """Dataset.
    """

    def __init__(self, d: Dict[str, str],
                 param_type: str = s.param_generic_type,
                 **kwargs):
        """__init__.

        Parameters
        ----------
        d : Dict[str, str]
            d
        param_type : str
            param_type
        kwargs :
            kwargs
        """
        self.origin = str(d[s.data_origin_key])
        self.operations = []
        self.args = d[s.param_action_args]
        self.kwargs = d[s.param_action_kwargs]
        if s.data_operations_key in d.keys():
            self.operations = ast.literal_eval(d[s.data_operations_key])
        super().__init__(d, param_type=s.dataset_obj_type, **kwargs)

        if '[' in self.value:
            self.value = ast.literal_eval(self.value)

        self.depends_on = None
        if self.origin in s.dst_origin_depends_on:
            if isinstance(self.value, str):
                self.depends_on = [self.value]
            elif isinstance(self.value, list):
                self.depends_on = self.value
            else:
                raise ValueError("The depends on must be a list or a string")

    def as_dst(self) -> Dict[str, Any]:
        """as_dst.

        Parameters
        ----------

        Returns
        -------
        Dict[str, Any]

        """
        return {
            s.data_origin_key: self.origin,
            s.param_value: self.value,
            s.data_operations_key: self.operations,
            s.param_action_args: self.args,
            s.param_action_kwargs: self.kwargs,
            s.param_depends_on_key: self.depends_on
        }

class CallableParam(TypeSpecific):
    """Callable.
    """


    def __init__(self, d: Dict[str, Any],
                 function: Callable = None,
                 **kwargs):
        """__init__.

        Parameters
        ----------
        d : Dict[str, Any]
            d
        function : Callable
            function
        kwargs :
            kwargs
        """
        self.args = d[s.param_action_args]
        self.kwargs = d[s.param_action_kwargs]
        if function is None:
            raise ValueError("The callable function must be provided!")
        self.function = function
        super().__init__(d, **kwargs)

    def __call__(self, *args, **kwargs) -> Any:
        """__call__.

        Parameters
        ----------
        args :
            args
        kwargs :
            kwargs

        Returns
        -------
        Any

        """
        # print(*args)
        # print(*kwargs)
        self.kwargs.update(kwargs)
        return self.function(self.value, *args, *self.args, **self.kwargs)

    def __str__(self) -> str:
        """__str__.

        Parameters
        ----------

        Returns
        -------
        str

        """
        super_input = super().__str__()
        return super_input + f" - args: {self.args} - kwargs: {self.kwargs}"
