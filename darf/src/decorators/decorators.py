# © 2025 Nokia
# Licensed under the BSD 3-Clause License
# SPDX-License-Identifier: BSD-3-Clause
#
# Contact: Mattia Milani (Nokia) <mattia.milani@nokia.com>

"""
Decorators Module
=================

This module takes care of all the decorators
"""

import functools
import inspect
from time import time
from typing import Callable, Dict, Any, Optional

from darf.src.log import LogHandler

plot_functions: Dict[str, Any] = {}
plot_legends: Dict[str, Any] = {}
interpolate_functions: Dict[str, Any] = {}
data_operations: Dict[str, Any] = {}
plot_operations: Dict[str, Any] = {}
data_loaders: Dict[str, Any] = {}
classes: Dict[str, Any] = {}

def get_real_name(obj: Any):
    """get_realName.

    Parameters
    ----------
    obj : Any
        obj
    """
    if obj.__name__ == "AugmentedCls":
        return obj.c_passed_name
    return obj.__qualname__

def collector(obj: Callable):
    """collector.

    Parameters
    ----------
    obj : Callable
        obj
    """
    @functools.wraps(obj)
    def wrapper(*args, **kwargs):
        """wrapper.

        Parameters
        ----------
        args :
            args
        kwargs :
            kwargs
        """
        return obj(*args, **kwargs)
    return wrapper

def plot(plot_function):
    """plot.

    Parameters
    ----------
    plot_function :
        plot_function
    """
    plot_functions[plot_function.__qualname__] = plot_function
    return collector(plot_function)

def interpolator(interpolate_fn):
    """interpolator.

    Parameters
    ----------
    interpolate_fn :
        interpolate_fn
    """
    interpolate_functions[interpolate_fn.__qualname__] = interpolate_fn
    return collector(interpolate_functions)

def data_op(data_op_fn):
    """data_op.

    Parameters
    ----------
    data_op_fn :
        data_op_fn
    """
    data_operations[data_op_fn.__qualname__] = data_op_fn
    return collector(data_operations)

def plot_op(plot_op_fn):
    """plot_op.

    Parameters
    ----------
    plot_op_fn :
        plot_op_fn
    """
    plot_operations[plot_op_fn.__qualname__] = plot_op_fn
    return collector(plot_operations)

def plot_legend(plot_lgnd_fn):
    """plot_legend.

    Decorator to include the function in the available plot legends
    dictionary

    Parameters
    ----------
    data_op_fn :
        data_op_fn
    """
    plot_legends[plot_lgnd_fn.__qualname__] =plot_lgnd_fn
    return collector(plot_legends)

def data_loader(data_loader_cls):
    """data_loader.

    Parameters
    ----------
    data_loader_cls :
        data_loader_cls
    """
    name = get_real_name(data_loader_cls)
    data_loaders[name] = data_loader_cls
    return collector(data_loader_cls)

def cls_wrapper(obj):
    """cls_wrapper.

    Parameters
    ----------
    obj :
        obj
    """
    classes[obj.__qualname__] = obj
    return collector(obj)

def c_logger(c_passed):
    """c_logger.

    Parameters
    ----------
    c_passed :
        c_passed
    """
    # pylint: disable=too-few-public-methods
    # this class is not supposed to expose any pubblic method other than the __init__
    class AugmentedCls(c_passed):
        """AugmentedCls.
        """

        c_passed_name = c_passed.__qualname__

        def __write_msg(self, msg: str, level: int = LogHandler.INFO):
            """__write_msg.

            Parameters
            ----------
            msg : str
                msg
            level : int
                level
            """
            if self.logger is None:
                return
            self.logger(f"{c_passed.__qualname__}", f"{msg}", level)

        def __init__(self, *args, logger: Optional[LogHandler] = None, **kwargs):
            """__init__.

            Parameters
            ----------
            args :
                args
            logger : Optional[LogHandler]
                logger
            kwargs :
                kwargs
            """
            self.logger = logger
            self.write_msg = self.__write_msg
            super().__init__(*args, **kwargs)

    return AugmentedCls

def f_logger(f_passed):
    """f_logger.

    Parameters
    ----------
    f_passed :
        f_passed
    """
    oldsig = inspect.signature(f_passed)
    params = list(oldsig.parameters.values())

    # def add_kwarg_assignment(name, f, idx=0):
    #     previous_code = f.__code__

    #     source_code = inspect.getsource(f)
    #     tree = ast.parse(source_code)
    #     print("----------------------")
    #     print(ast.dump(tree))

    #     comment = None
    #     slice=ast.Index(ast.Constant(name, None))
    #     value=ast.Subscript(ast.Name("kwargs", ast.Load()), slice, ast.Load())
    #     targets = [ast.Name(name, ast.Store())]
    #     log_assign = ast.Assign(targets, value, comment)
    #     tree.body[0].body.insert(idx, log_assign)
    #     ast.fix_missing_locations(tree)

    #     new_code_obj = compile(tree, previous_code.co_filename, 'exec')
    #     print(new_code_obj.co_consts)
    #     f.__code__ = new_code_obj.co_consts[-2]
    #     source_code = inspect.getsource(f)
    #     tree = ast.parse(source_code)
    #     print("----------------------")
    #     print(ast.dump(tree))
    #     # globals = f.__globals__
    #     # f.__code__.replace(new_code_obj)
    #     # exec_scope = {}

    #     # exec(new_code_obj, globals, exec_scope)
    #     # print("--------- exec scope -----------")
    #     # print(exec_scope)
    #     return f
    #     # new_function = FunctionType(new_code_obj.co_consts[-2], f.__globals__)

    def __dummy_log():
        """__dummy_log.

        Parameters
        ----------
        self :
            self
        args :
            args
        kwargs :
            kwargs
        """

    def add_kwarg(name, default, f=None):
        """add_kwarg.

        Parameters
        ----------
        name :
            name
        default :
            default
        f :
            f
        """
        if f is None:
            f = f_passed

        if name in oldsig.parameters:
            raise ValueError(f"logger parameter already present in \
                    {f_passed.__qualname__} signature")

        position = len(params)
        for i, param in enumerate(params):
            if param.kind == inspect.Parameter.VAR_KEYWORD:
                position = i
                break

        newparam = inspect.Parameter(name,
                                     inspect.Parameter.KEYWORD_ONLY,
                                     default = default)
        params.insert(position, newparam)
        # new_f = add_kwarg_assignment(name, f=f)
        # return new_f

    add_kwarg("logger", None)
    # print(astor.to_source(inspect.getsource(new_f)))
    add_kwarg("write_msg", __dummy_log)
    # print(astor.to_source(inspect.getsource(new_f)))

    sig = oldsig.replace(parameters = params)

    @functools.wraps(f_passed)
    def wrapper(*args, logger: Optional[LogHandler] = None, **kwargs):
        """wrapper.

        Parameters
        ----------
        args :
            args
        logger : Optional[LogHandler]
            logger
        kwargs :
            kwargs
        """
        bound = sig.bind(*args, **kwargs)
        bound.apply_defaults()

        def __write_msg(msg: str, level: int = LogHandler.INFO):
            """__write_msg.

            Parameters
            ----------
            msg : str
                msg
            level : int
                level
            """
            if logger is None:
                return
            logger(f"{f_passed.__qualname__}", f"{msg}", level)

        bound.arguments["logger"] = logger
        bound.arguments["write_msg"] = __write_msg
        return f_passed(*bound.args, **bound.kwargs)

    wrapper.__signature__ = sig
    return wrapper

def timeit(func):
    """timeit.

    Parameters
    ----------
    func :
        func
    """

    @functools.wraps(func)
    @f_logger
    def new_func(*args, **kwargs):
        """new_func.

        Parameters
        ----------
        args :
            args
        kwargs :
            kwargs
        """
        _, write_msg = kwargs["logger"], kwargs["write_msg"]
        del kwargs["logger"]
        del kwargs["write_msg"]

        start_time = time()
        res = func(*args, **kwargs)
        delta_t = time() - start_time
        write_msg(f"Function {func.__name__} finished in {int(delta_t*1000)} ms", LogHandler.DEBUG)
        # print(f"Function {func.__name__} finished in {int(delta_t*1000)} ms")
        return res
    return new_func
