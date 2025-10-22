# © 2025 Nokia
# Licensed under the BSD 3-Clause License
# SPDX-License-Identifier: BSD-3-Clause
#
# Contact: Mattia Milani (Nokia) <mattia.milani@nokia.com>

"""
progress bar module
===================

Module used to set the progress bar properly across the whole framework

"""

import os
from tqdm import tqdm

class Pb:
    """pb.
    Class used to manage the progress bar
    """

    silent = False

    @classmethod
    def tq_bar(cls, *args, **kwargs):
        """bar.
        Define a normal bar

        Parameters
        ----------
        args :
            args
        kwargs :
            kwargs
        """
        if cls.silent:
            return tqdm(*args, file=open(os.devnull, "w", encoding="utf8"), **kwargs)
        return tqdm(*args, **kwargs)

    @classmethod
    def databar(cls, num, *args, **kwargs) -> tqdm:
        """databar.
        Define a specific data bar formatted in a specific way

        Parameters
        ----------
        num :
            num
        args :
            args
        kwargs :
            kwargs
        """
        return tqdm(*args, **kwargs, ascii=True, total=num,
                    bar_format="{desc} {n_fmt}/{total_fmt} [{elapsed}]{postfix}\033[0m")

    @classmethod
    def success_close(cls,
                      pbar: tqdm,
                      msg: str):
        """close_bar.
        Close the bar

        Parameters
        ----------
        bar : tqdm
            bar
        """
        pbar.set_description_str(f"\033[0;32m✔️  {msg}\033[0m")
        pbar.set_postfix_str("                                                      ", refresh=True)
        pbar.clear()
        pbar.refresh()
        pbar.close()
