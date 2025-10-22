# © 2025 Nokia
# Licensed under the BSD 3-Clause License
# SPDX-License-Identifier: BSD-3-Clause
#
# Contact: Mattia Milani (Nokia) <mattia.milani@nokia.com>

"""
Sankey Module
=============

Operations to transform a dataset in raw format to a sankey digestable format.
"""

from typing import List, Any

import re
import numpy as np
import pandas as pd

from darf.src.decorators import data_op


def transition(df, source_it, dst_it,
               it_clm: str = "Iteration",
               flag_clm: str = "Flag",
               id_clm: str = "SampleID") -> tuple:
	source_df = df[df[it_clm] == source_it]
	dst_df = df[df[it_clm] == dst_it]
	source_g_df = source_df[source_df[flag_clm] == 0.0]
	source_b_df = source_df[source_df[flag_clm] == 1.0]
	source_u_df = source_df[source_df[flag_clm] == 2.0]
	dst_g_df = dst_df[dst_df[flag_clm] == 0.0]
	dst_b_df = dst_df[dst_df[flag_clm] == 1.0]
	dst_u_df = dst_df[dst_df[flag_clm] == 2.0]

	source_g_ids = source_g_df[id_clm].values
	source_b_ids = source_b_df[id_clm].values
	source_u_ids = source_u_df[id_clm].values
	dst_g_ids = dst_g_df[id_clm].values
	dst_b_ids = dst_b_df[id_clm].values
	dst_u_ids = dst_u_df[id_clm].values

	src_g_dst_g = len(np.intersect1d(source_g_ids, dst_g_ids))
	src_g_dst_b = len(np.intersect1d(source_g_ids, dst_b_ids))
	src_g_dst_u = len(np.intersect1d(source_g_ids, dst_u_ids))
	src_b_dst_g = len(np.intersect1d(source_b_ids, dst_g_ids))
	src_b_dst_b = len(np.intersect1d(source_b_ids, dst_b_ids))
	src_b_dst_u = len(np.intersect1d(source_b_ids, dst_u_ids))
	src_u_dst_g = len(np.intersect1d(source_u_ids, dst_g_ids))
	src_u_dst_b = len(np.intersect1d(source_u_ids, dst_b_ids))
	src_u_dst_u = len(np.intersect1d(source_u_ids, dst_u_ids))

	sources = [
	            f"G{source_it}", f"B{source_it}", f"U{source_it}",
	            f"G{source_it}", f"B{source_it}", f"U{source_it}",
	            f"G{source_it}", f"B{source_it}", f"U{source_it}",
	          ]
	destinations = [
	                f"G{dst_it}", f"G{dst_it}", f"G{dst_it}",
	                f"B{dst_it}", f"B{dst_it}", f"B{dst_it}",
	                f"U{dst_it}", f"U{dst_it}", f"U{dst_it}",
	               ]
	values = [
	            src_g_dst_g, src_b_dst_g, src_u_dst_g,
	            src_g_dst_b, src_b_dst_b, src_u_dst_b,
	            src_g_dst_u, src_b_dst_u, src_u_dst_u,
	         ]
	return sources, destinations, values

@data_op
def df2sankey(df: pd.DataFrame,
              flag_clm: str = "Flag",
              iter_clm: str = "Iteration",
              id_clm: str = "SampleID",
              it_start: int = 0,
              it_end: int = 8,
              start_label: str = 'U',
              labels: List[str] = ['G', 'B', 'U'],
              val_labels: List[Any] = [0.0, 1.0, 2.0]) -> pd.DataFrame:
    if flag_clm not in df.columns:
        raise ValueError(f"Column '{flag_clm}' not found in the dataframe.")

    node_labels = [start_label]
    for i in range(it_start, it_end+1):
        for label in labels:
            node_labels.append(f"{label}{i}")

    node_dict = {label: i for i, label in enumerate(node_labels)}

    sources = [start_label]*len(labels)
    destinations = [f"{label}{it_start}" for label in labels]
    values = [len(df[(df[flag_clm] == val) & (df[iter_clm] == it_start)]) for val in val_labels]
    print(values)

    for src, dst in zip(range(it_start, it_end),range(it_start+1,it_end+1)):
        s, d, v = transition(df, src, dst, it_clm=iter_clm, flag_clm=flag_clm, id_clm=id_clm)
        sources.extend(s)
        destinations.extend(d)
        values.extend(v)

    source_node = [node_dict[x] for x in sources]
    target_node = [node_dict[x] for x in destinations]
    source_class = [re.sub(r'\d+', '', s) for s in sources]
    target_class = [re.sub(r'\d+', '', s) for s in destinations]

    iterations = [0]*len(labels) + [i for i in range(it_start+1, it_end+2) for _ in range((len(labels)*len(labels))-1)]

    assert len(source_node) == len(target_node) == len(values) == len(source_class) == len(target_class) == len(iterations)

    sankey_df = pd.DataFrame({
        'source': source_node,
        'source_class': source_class,
        'target': target_node,
        'target_class': target_class,
        'value': values,
        'Iteration': iterations
    })

    return sankey_df