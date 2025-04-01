# © 2025 Nokia
# Licensed under the BSD 3-Clause License
# SPDX-License-Identifier: BSD-3-Clause
#
# Contact: Mattia Milani (Nokia) <mattia.milani@nokia.com>

"""
Operations obj Module
=====================

This module contains the operations object.
This object can be used to create operations dictionaries on the fly.
"""

from typing import Dict, Any, List, Union, Self

from darf.src.params import ParamHandler as PH
from darf.src.util.strings import s

class Operations():

    def __init__(self, operations: Dict[str, Dict[str, Any]]):
        """__init__.

        function to generate the operations object.
        It takes as input a Dictionary of operations, where each key
        identify a different operation.
        Each operation is identified by it's name.
        The attributes in the dictionary describes how the operation
        is going to be applied.
        There is one mandatory field that should be in the operation
        object:
            - operation: the function to call
        The optional fieds int he dictionary are:
            - args: the arguments to pass to the function
            - kwargs: the keyword arguments to pass to the function
        If those arguments are not present then a default empty Tuple and Dict
        will be used respectively.

        Types accepted:
            - Operation key: must be a string
            - Operation function: must be a function
            - Operation args: must be a Tuple
            - Operation kwargs: must be a Dict
        If different types are provided an exception will be raised.

        All other keys in the operation dictionary will be discarded.

        Parameters
        ----------
        operations : Dict[str, Dict[str, Any]]
            The dictionary of operations, the first level key identifies
            the operation, the second level keys are the attributes of the
            operation.

        Raises
        ------
        ValueError
            If the types of the values are not the expected ones
        """

        self.__approved_keys = [s.io_type_key,
                                s.param_value,
                                s.param_action_args,
                                s.param_action_kwargs]
        self.__sanity_check_full_set(operations)

        self.dict = operations
        op_list = [{s.io_name_key: key, **value} for key, value in operations.items()]

        self.op_h = PH(op_list, None)

    def __sanity_check_full_set(self, operations: Dict[str, Dict[str, Any]]):
        """__sanity_check.

        Function to check the sanity of the operations dictionary.

        Parameters
        ----------
        operations : Dict[str, Dict[str, Any]]
            The dictionary of operations

        Raises
        ------
        ValueError
            If the types of the values are not the expected ones
        """
        for key, value in operations.items():
            if not isinstance(key, str):
                raise ValueError(f"Operation key must be a string, got {type(key)}")
            if not isinstance(value, dict):
                raise ValueError(f"Operation value must be a dictionary, got {type(value)}")
            self.__sanity_check_single(value)

    def __sanity_check_single(self, operation: Dict[str, Any]):
        """__sanity_check_single.

        Function to check the sanity of a single operation dictionary.

        Parameters
        ----------
        operation : Dict[str, Any]
            The dictionary of a single operation

        Raises
        ------
        ValueError
            If the types of the values are not the expected ones
        """
        if s.param_value not in operation.keys():
            raise ValueError(f"Operation must have a {s.param_value} key")

        if s.param_action_args not in operation.keys():
            operation[s.param_action_args] = ()
        if s.param_action_kwargs not in operation.keys():
            operation[s.param_action_kwargs] = {}

        operation[s.io_type_key] = s.param_op_type

        operation = {k: v for k, v in operation.items() if k in self.__approved_keys}

        if not isinstance(operation[s.param_value], str):
            raise ValueError(f"Operation name must be a string, got {type(operation[s.io_name_key])}")
        if not isinstance(operation[s.param_action_args], tuple):
            raise ValueError(f"Operation args must be a Tuple, got {type(operation[s.param_action_args])}")
        if not isinstance(operation[s.param_action_kwargs], dict):
            raise ValueError(f"Operation kwargs must be a Dict, got {type(operation[s.param_action_kwargs])}")

    @classmethod
    def one(cls, name: str, operation_function: str, *args, **kwargs):
        """one.

        This class method provides the capability to easily create an operation
        object with just one element inside.

        Parameters
        ----------
        name : str
            The name of the operation
        operation_function : str
            The function to call
        args :
            args to pass to the function when called
        kwargs :
            kwargs to pass to the function when called

        Returns
        -------
        Operation
            The operation object
        """
        return cls({name: {s.param_value: operation_function,
                           s.param_action_args: args,
                           s.param_action_kwargs: kwargs}})

    @classmethod
    def concat(cls, *operations: Union[List[Self], set]):
        """concat.

        This class method provides the capability to easily concatenate multiple
        operations objects into one.

        Parameters
        ----------
        operations : List[Operations]
            The list of operations to concatenate

        Returns
        -------
        Operations
            The concatenated operations object

        Raises
        ------
        ValueError
            If there is an overlap of operation keys in the operations
        """
        op_dict = {}
        for operation in operations:
            # If there is an overlap of keys then raise an exception
            if set(op_dict.keys()).intersection(set(operation.dict.keys())):
                raise ValueError("There is an overlap of operation keys in the operations")
            op_dict.update(operation.dict)
        return cls(op_dict)

    def __call__(self, name: str, *args, **kwargs):
        return self.op_h.get_handler(name)(*args, **kwargs)

    def __str__(self):
        return str(self.dict)
