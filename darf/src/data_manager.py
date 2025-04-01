# © 2025 Nokia
# Licensed under the BSD 3-Clause License
# SPDX-License-Identifier: BSD-3-Clause
#
# Contact: Mattia Milani (Nokia) <mattia.milani@nokia.com>

"""
class module
============

Use this module to manage a class object.
"""

from typing import Any, Dict, List, Self, Optional

import pandas

from darf.src.params import ParamHandler as PH
from darf.src.util.strings import s
from darf.src.io import Pb as pb
from darf.src.io import PickleHandler as PkH
from darf.src.data_loader.loader import cls_loader as loader
from darf.src.util import compute_hash
from darf.src.decorators import c_logger
from .operations_obj import Operations

@c_logger
class Dataset:
    """Dataset.

    Class used to handle a single dataset object

    The dataset follows the lazy evaluation concept, the data will be
    effectively loaded only when requested.
    """

    # pylint: disable=too-many-instance-attributes, too-many-arguments, too-many-positional-arguments
    # The number of attributes still looks reasonable in this particular
    # case.
    def __init__(self, obj: Dict[str, Any],
                 key: Optional[str] = None,
                 operations: Optional[PH] = None,
                 pklh: Optional[PkH] = None,
                 force: bool = False):
        """__init__.

        Parameters
        ----------
        obj : Dict[str, Any]
            object to load with all the properties
        key : Optional[str]
            key of the object, if the key is not provided then it will
            be generated as hash of the object passed.
        operations : Optional[PH]
            operations object, if None no operations will be applied
        pklh : Optional[PkH]
            pickle handler object, if None no pkl file will be saved or loaded
        force : bool
            force the recomputation of the dataset at each request
        """
        self.obj = self.__parse_obj(obj)
        self.key = compute_hash(str(self.obj), digest_size=8) if key is None else key
        self.oph = operations
        self.pkh = pklh
        self.force = force
        self.depends_on = self.__define_dependencies()
        self.__data = None
        self.hash = None if "hash" not in obj.keys() else obj["hash"]

    def __parse_obj(self, obj: Dict[str, Any]) -> Dict[str, Any]:
        """__parse_obj.
        This function is used to parse the input dictionary and load
        all the filds with the default values if not provided.
        Two mandatory fileds are:
            - origin: the origin of the dataset, which identifies the type of
                      data loader that will be used
            - value: the value of the dataset, which is passed to the loader.

        If one of those two values is not present an exception will be raised.

        Other available paramters are:
            - operations: list of operations to apply to the dataset
            - depends_on: list of keys that this dataset depends on
            - args: arguments to pass to the loader, this is expected to be a
                    set, if 'args' is provided but it's not a tuple then
                    an exception will be raised.
            - kwargs: keyword arguments to pass to the loader, this is expected
                      to be a dictionary, if 'kwargs' is provided but it's not
                      a dictionary then an exception will be raised.
            - hash: fixed hash to use for the dataset

        Any other parameters will be ignored.

        Parameters
        ----------
        obj : Dict[str, Any]
            dictionary to parse

        Returns
        -------
        Dict[str, Any]
            parsed dictionary with only the allowed parameters

        Raises
        ------
        ValueError
            If the origin or the value are not present
            If the args parameter is not a tuple and it's provided
            If the kwargs parameter is not a dictionary and it's provided
        """
        if s.data_origin_key not in obj.keys() or \
                s.param_value not in obj.keys():
            raise ValueError("The origin and the value must be provided")

        if s.param_action_args in obj.keys() and \
                not isinstance(obj[s.param_action_args], tuple):
            raise ValueError("The args parameter must be a set")

        if s.param_action_kwargs in obj.keys() and \
                not isinstance(obj[s.param_action_kwargs], dict):
            raise ValueError("The kwargs parameter must be a dictionary")

        return {
            s.data_origin_key: obj[s.data_origin_key],
            s.param_value: obj[s.param_value],
            s.data_operations_key: obj[s.data_operations_key]
            if s.data_operations_key in obj.keys() else [],
            s.param_action_args: obj[s.param_action_args]
            if s.param_action_args in obj.keys() else set(),
            s.param_action_kwargs: obj[s.param_action_kwargs]
            if s.param_action_kwargs in obj.keys() else {},
            s.param_depends_on_key: obj[s.param_depends_on_key]
            if s.param_depends_on_key in obj.keys() else None,
            "hash": obj["hash"] if "hash" in obj.keys() else None
        }

    def __define_dependencies(self) -> Optional[Dict[str, Any]]:
        """__define_dependencies.

        Define the dependencies of the dataset

        Parameters
        ----------

        Returns
        -------
        Dict[str, Any]
            dictionary of dependencies or None
        """
        if s.param_depends_on_key not in self.obj.keys() or \
                self.obj[s.param_depends_on_key] is None:
            return None

        return {key: None for key in self.obj[s.param_depends_on_key]}

    def __load_pkl(self) -> Optional[int]:
        """__load_pkl.
        Load the pkl file if it exists and the hash is correct

        Parameters
        ----------

        Returns
        -------
        Optional[int]
            None if the file is not loaded, 1 if the file is loaded

        """
        if self.pkh is None:
            return None
        if self.force:
            return None
        if not self.pkh.check(self.key, custom_hash=self.hash):
            return None
        self.__data = self.pkh.load(self.key, custom_hash=self.hash)
        return 1

    def __save_data(self) -> Optional[int]:
        """__save_data.
        Save the data to a pkl file

        Parameters
        ----------

        Returns
        -------
        Optional[int]
            None if the file is not saved, 1 if the file is saved
        """
        if self.pkh is None:
            return None
        self.pkh.save(self.__data, self.key, custom_hash=self.hash,
                      override=self.force)
        return 1

    def __compute(self) -> None:
        """__compute.

        Compute the dataset and save it to a pkl file if possible.
        the computation follows the following steps:
            - Get the hash
            - Load the pkl file if possible
            - Load the dataset
            - Apply the operations
            - Save the dataset to a pkl file if possible
        The dataset is saved into self.data

        Parameters
        ----------

        Returns
        -------
        None
        """
        pbar = pb.databar(1, desc=f"Loading input dataset {self.key} ...",
                          leave=False)

        self.hash = self.__get_hash() if self.hash is None else self.hash

        if self.__load_pkl() is not None:
            return

        self.load_df()
        self.apply_operations()

        self.__save_data()

        pbar.close()

    def load_df(self) -> None:
        """load_df.
        Load the dataset from the origin

        Parameters
        ----------

        Returns
        -------
        None

        """
        origin = self.obj[s.data_origin_key]
        value = self.obj[s.param_value] if self.depends_on is None else self.depends_on
        obj_args = self.obj[s.param_action_args]
        obj_kwargs = self.obj[s.param_action_kwargs]
        self.__data = loader(origin, value, pklh=self.pkh)(*obj_args, **obj_kwargs)

    def apply_operations(self) -> None:
        """apply_operations.
        Apply the operations to the dataset
        If the operations are not present or empty the function will have no
        effect

        Parameters
        ----------

        Returns
        -------
        None

        """
        operations = self.obj[s.data_operations_key]

        if not isinstance(operations, list) or len(operations) == 0:
            return

        op_bar = pb.databar(len(operations), desc="Appling operations ... ",
                            leave=False)
        for op in operations:
            self.write_msg(f"Applying operation: {op}")
            op_bar.set_description_str(f"Applying operation: {op} ")

            if isinstance(self.oph, PH):
                self.__data = self.oph.get_handler(op)(self.__data)
            elif isinstance(self.oph, Operations):
                self.__data = self.oph(op, self.__data)

            op_bar.update(1)
        op_bar.close()

    def __get_hash(self, digest_size: int = 8) -> str:
        """__get_dst_hash.
        Generate the hash of a dataset object, using the key name and
        the attributes, but not the dataset iteself.

        Parameters
        ----------
        digest_size : int
            size of the digest

        Returns
        -------
        str
            hash
        """
        obj_str = str(self.obj).join(self.key)
        return compute_hash(obj_str, digest_size=digest_size)

    @property
    def data(self) -> pandas.DataFrame:
        """data.
        Returns the dataset, if the dataset has not been computed yet
        the function will compute it.

        Parameters
        ----------

        Returns
        -------
        pandas.DataFrame

        """
        if self.__data is None:
            self.__compute()
        return self.__data


@c_logger
class DatasetManager:
    """DatasetManager.

	General object to manage datasets
    Manipulation functions should be managed inside the data_operations folder
	"""

    def __init__(self, data: Dict[str, Dict[str, Any]],
                 force: bool = False,
                 operations: PH = None,
                 pklh: Optional[PkH] = None):
        """__init__.

        Parameters
        ----------
        data : Dict[str, Dict[str, Any]]
            data
        force : bool
            force
        operations : PH
            operations
        pklh : Optional[PkH]
            pklh
        """
        self.oph = operations
        self.pkh = pklh
        self.force = force
        self.data: Dict[str, Dict[str, Any]] = {}

        for key, obj in data.items():
            self.__define_dataobj(key, obj)

    def __define_dataobj(self, key: str, obj: Dict[str, Any]) -> None:
        """__define_dataobj.

        Parameters
        ----------
        key : str
            key
        obj : Dict[str, Any]
            obj

        Returns
        -------
        None

        """
        self.data[key] = Dataset(obj, key=key, operations=self.oph,
                                 pklh=self.pkh, force=self.force,
                                 logger=self.logger)

    @classmethod
    def from_cfg(cls, conf: PH, *args, **kwargs) -> Self:
        """from_cfg.

        Parameters
        ----------
        conf : PH
            conf
        args :
            args
        kwargs :
            kwargs

        Returns
        -------
        Self

        """
        pbar = pb.databar(len(conf.objects.keys()),
                            desc="Parsing input datasets ...")
        items = {}
        for key in conf.objects.keys():
            d = conf.objects[key]
            if d.type not in s.dataset_obj_types:
                pbar.update(1)
                continue

            if d.origin not in s.all_dst_origin:
                raise ValueError(f"Unknown origin {d.origin}")

            items[key] = d.as_dst()
            pbar.update(1)

        pb.success_close(pbar, "Dataset parsing compleated")
        return cls(items, *args, **kwargs)

    def __getitem__(self, item: str) -> pandas.DataFrame:
        """__getitem__.

        Parameters
        ----------
        item : str
            item

        Returns
        -------
        pandas.DataFrame

        """
        if self.data[item].depends_on is not None and \
                len(self.data[item].depends_on) > 0:
            self.write_msg(f"Loading dataset: {item} - Depends on: {self.data[item].depends_on}")
            for dep in self.data[item].depends_on:
                self.data[item].depends_on[dep] = self[dep]
        return self.data[item].data

    def keys(self) -> List[str]:
        """keys.

        Returns
        -------
        List[str]
            list of keys

        """
        return list(self.data.keys())

    def show(self, df_request: Optional[List[str]] = None) -> None:
        """show_data.

        Parameters
        ----------
        df_request : List[str]
            list of keys to show

        """
        df_request = [] if df_request is None else df_request

        if len(df_request) == 0:
            df_request = self.keys()

        for key in df_request:
            # df = self[key][['op_id', 'timestamp', 'good_dst', 'bad_dst']].reset_index()
            # print(f"Data: {key}\n{df.loc[140:160]}")
            print(f"Data: {key}\n{self[key]}")
            print(f"Data info:\n {self[key].shape}")
            print(f"Data types:\n {self[key].dtypes}")
            print("------------------------")
            # l_low = 30.0
            # l_high = 70.0
            # df_bad_p_in_range = self[key].loc[(self[key]['bad_p'] >= l_low) & (self[key]['bad_p'] <= l_high)]
            # # print(f"Data bad_p in ({l_low} and {l_high}): {df_bad_p_in_range[['op_id', 'timestamp', 'bad_p', 'Height']]}")
            # tot_samples = self[key].shape[0]
            # n_bad_p = df_bad_p_in_range.shape[0]
            # print(f"Num of bad_p in ({l_low} and {l_high}): {n_bad_p}/{tot_samples}")
            # print(f"Percentage of bad_p in ({l_low} and {l_high}): {n_bad_p*100.0/tot_samples:.2f}/100")
            # print("------------------------")
            # min_height = 0.75
            # df_bad_p_min_height = df_bad_p_in_range.loc[df_bad_p_in_range['Height'] >= min_height]
            # # print(f"Data bad_p in ({l_low} and {l_high}, min h {min_height}): {df_bad_p_min_height[['op_id', 'timestamp', 'bad_p', 'Height']]}")
            # tot_samples = self[key].shape[0]
            # n_bad_p = df_bad_p_min_height.shape[0]
            # print(f"Num of bad_p in ({l_low} and {l_high}, min h {min_height}): {n_bad_p}/{tot_samples}")
            # print(f"Percentage of bad_p in ({l_low} and {l_high}, min h {min_height}): {n_bad_p*100.0/tot_samples:.2f}/100")
            # print("------------------------")
