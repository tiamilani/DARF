# © 2025 Nokia
# Licensed under the BSD 3-Clause License
# SPDX-License-Identifier: BSD-3-Clause
#
# Contact: Mattia Milani (Nokia) <mattia.milani@nokia.com>

"""
aggregate Module
================

Contains operations relatives to the aggregation of dataframes clm/rws
"""

from typing import List, Optional

import pandas as pd

from darf.src.decorators import data_op

# pylint: disable=too-many-arguments
@data_op
def aggregate_cm(df: pd.DataFrame,
                 grp_id: Optional[List[str]] = None,
                 cm_id: str = "cm",
                 stats: Optional[List[str]] = None,
                 output_val: str = "Value",
                 end_drop: Optional[List[str]] = None) -> pd.DataFrame:
    """aggregate_cm.
    Aggregate the confusion matrix data.
    Use id as groupby columns identifiers
    Computes N stats that will be included into the cm_id column and the
    value in output_val.

    Parameters
    ----------
    df : pd.DataFrame
        The input data
    grp_id : List[str]
        List of id columns for the group by
    cm_id : str
        The column name for the confusion matrix statistics, where TP FP FN TN U and
        expected_P, expected_N are located
    stats : List[str]
        List of statistics to compute
    output_val : str
        The column name for the output value
    end_drop : List[str]
        List of columns to drop at the end of the aggregation
    """
    grp_id = grp_id if not grp_id is None else []
    stats = stats if not stats is None else []
    end_drop = end_drop if not end_drop is None else ["level_2"]

    assert len(stats) > 0
    stat_dfs = []
    for stat in stats:
        tmp_df = df.groupby(grp_id)[[cm_id, output_val]].apply(
                lambda x: compute_cm(x, stat, cm_id=cm_id, output_val=output_val)
            )
        tmp_df.reset_index(inplace=True)
        tmp_df.drop(columns=end_drop, inplace=True)
        # replace possible NaN with 0.0
        tmp_df.fillna(0.0, inplace=True)
        stat_dfs.append(tmp_df)
    return pd.concat(stat_dfs)

def compute_cm(x: pd.DataFrame, stat: str,
               cm_id: str = "cm",
               output_val: str = "Value") -> pd.DataFrame:
    """compute_cm.
    Compute the confusion matrix statistics.

    Parameters
    ----------
    x : pd.DataFrame
        The input data
    stat : str
        The statistic to compute
    cm_id : str
        The column name for the confusion matrix statistics, where TP FP FN TN U and
        expected_P, expected_N are located
    output_val : str
        The column name for the output value

    Returns
    -------
    pd.DataFrame

    Raises
    ------
    ValueError
        If the stat is not implemented
    """
    res = None
    corct_lbl = ["TP", "TN"]
    expect_lbl = ["expected_P", "expected_N"]

    match stat:
        case 'Accuracy':
            res = cm_accuracy(x, cm_id=cm_id, output_val=output_val,
                              expected_lbl=expect_lbl, crct_lbl=corct_lbl)
        case 'Precision':
            res = cm_precision(x, cm_id=cm_id, output_val=output_val)
        case 'Recall':
            res = cm_recall(x, cm_id=cm_id, output_val=output_val)
        case 'Specificity':
            res = cm_specificity(x, cm_id=cm_id, output_val=output_val)
        case 'Fall-Out':
            res = cm_fallout(x, cm_id=cm_id, output_val=output_val)
        case 'F1':
            res = cm_f1(x, cm_id=cm_id, output_val=output_val)
        case 'TP' | 'FP' | 'FN' | 'TN' | 'U':
            res = cm_specific(x, cm_id=cm_id, output_val=output_val, stat_name=stat)
        case _:
            raise ValueError(f"Stat {stat} not implemented")
    return res

def cm_accuracy(x: pd.DataFrame, cm_id: str = "cm",
                output_val: str = "Value",
                stat_name: str = "Accuracy",
                expected_lbl: Optional[List[str]] = None,
                crct_lbl: Optional[List[str]] = None) -> pd.DataFrame:
    """cm_accuracy.
    Compute the accuracy of the confusion matrix.

    Parameters
    ----------
    x : pd.DataFrame
        The input data
    cm_id : str
        The column name for the confusion matrix statistics, where TP FP FN TN U and
        expected_P, expected_N are located
    output_val : str
        The column name for the output value
    stat_name : str
        The name of the statistic
    expected_lbl : List[str]
        List of expected labels
    crct_lbl : List[str]
        List of correct labels

    Returns
    -------
    pd.DataFrame
    """
    crct_lbl = ["TP", "TN"] if crct_lbl is None else crct_lbl
    expected_lbl = ["expected_P", "expected_N"] if expected_lbl is None else expected_lbl

    tot = x[x[cm_id].isin(expected_lbl)][output_val].sum()
    correct = x[x[cm_id].isin(crct_lbl)][output_val].sum()
    accuracy = correct/tot if tot > 0 else 0.0
    return pd.DataFrame({cm_id: stat_name, output_val: [accuracy]})

def cm_precision(x: pd.DataFrame, cm_id: str = "cm",
                 output_val: str = "Value",
                 stat_name: str = "Precision") -> pd.DataFrame:
    """cm_precision.
    Compute the precision of the confusion matrix.

    Parameters
    ----------
    x : pd.DataFrame
        The input data
    cm_id : str
        The column name for the confusion matrix statistics, where TP FP FN TN U and
        expected_P, expected_N are located
    output_val : str
        The column name for the output value
    stat_name : str
        The name of the statistic

    Returns
    -------
    pd.DataFrame
    """
    tp = x[x[cm_id] == "TP"][output_val].sum()
    fp = x[x[cm_id] == "FP"][output_val].sum()
    precision = tp/(tp+fp) if (tp+fp) > 0 else 0.0
    return pd.DataFrame({cm_id: stat_name, output_val: [precision]})

def cm_recall(x: pd.DataFrame, cm_id: str = "cm",
              output_val: str = "Value",
              stat_name: str = "Recall") -> pd.DataFrame:
    """cm_recall.
    Compute the recall of the confusion matrix.

    Parameters
    ----------
    x : pd.DataFrame
        The input data
    cm_id : str
        The column name for the confusion matrix statistics, where TP FP FN TN U and
        expected_P, expected_N are located
    output_val : str
        The column name for the output value
    stat_name : str
        The name of the statistic

    Returns
    -------
    pd.DataFrame
    """
    tp = x[x[cm_id] == "TP"][output_val].sum()
    fn = x[x[cm_id] == "FN"][output_val].sum()
    recall = tp/(tp+fn) if (tp+fn) > 0 else 0.0
    return pd.DataFrame({cm_id: stat_name, output_val: [recall]})

def cm_specificity(x: pd.DataFrame, cm_id: str = "cm",
                   output_val: str = "Value",
                   stat_name: str = "Specificity") -> pd.DataFrame:
    """cm_specificity.
    Compute the specificity of the confusion matrix.

    Parameters
    ----------
    x : pd.DataFrame
        The input data
    cm_id : str
        The column name for the confusion matrix statistics, where TP FP FN TN U and
        expected_P, expected_N are located
    output_val : str
        The column name for the output value
    stat_name : str
        The name of the statistic

    Returns
    -------
    pd.DataFrame
    """
    tn = x[x[cm_id] == "TN"][output_val].sum()
    fn = x[x[cm_id] == "FN"][output_val].sum()
    specificity = tn/(tn+fn) if (tn+fn) > 0 else 0.0
    return pd.DataFrame({cm_id: stat_name, output_val: [specificity]})

def cm_fallout(x: pd.DataFrame, cm_id: str = "cm",
               output_val: str = "Value",
               stat_name: str = "Fall-Out") -> pd.DataFrame:
    """cm_fallout.
    Compute the fallout of the confusion matrix.

    Parameters
    ----------
    x : pd.DataFrame
        The input data
    cm_id : str
        The column name for the confusion matrix statistics, where TP FP FN TN U and
        expected_P, expected_N are located
    output_val : str
        The column name for the output value
    stat_name : str
        The name of the statistic

    Returns
    -------
    pd.DataFrame
    """
    fp = x[x[cm_id] == "FP"][output_val].sum()
    tn = x[x[cm_id] == "TN"][output_val].sum()
    fallout = fp/(fp+tn) if (fp+tn) > 0 else 0.0
    return pd.DataFrame({cm_id: stat_name, output_val: [fallout]})

def cm_f1(x: pd.DataFrame, cm_id: str = "cm",
          output_val: str = "Value",
          stat_name: str = "F1") -> pd.DataFrame:
    """cm_f1.
    Compute the F1 score of the confusion matrix.

    Parameters
    ----------
    x : pd.DataFrame
        The input data
    cm_id : str
        The column name for the confusion matrix statistics, where TP FP FN TN U and
        expected_P, expected_N are located
    output_val : str
        The column name for the output value
    stat_name : str
        The name of the statistic

    Returns
    -------
    pd.DataFrame
    """
    tp = x[x[cm_id] == "TP"][output_val].sum()
    fp = x[x[cm_id] == "FP"][output_val].sum()
    fn = x[x[cm_id] == "FN"][output_val].sum()
    f1 = 2*tp/(2*tp+fp+fn) if (2*tp+fp+fn) > 0 else 0.0
    return pd.DataFrame({cm_id: stat_name, output_val: [f1]})

def cm_specific(x: pd.DataFrame, cm_id: str = "cm",
                output_val: str = "Value",
                stat_name: str = "TP",
                expected_lbl: Optional[List[str]] = None) -> pd.DataFrame:
    """cm_specific.

    Compute the specific CM value reuqested.
    Available values are TP, FP, TN, FN, U.

    Parameters
    ----------
    x : pd.DataFrame
        The input data
    cm_id : str
        The column name for the confusion matrix statistics
    output_val : str
        The column name for the output value
    stat_name : str
        The name of the statistic could be TP FP FN TN U
    expected_lbl : List[str]
        Where to find the expected labels.

    Returns
    -------
    pd.DataFrame

    Raises
    ------
    ValueError
        If the stat_name is not in the available values
    """
    if stat_name not in ["TP", "FP", "FN", "TN", "U"]:
        raise ValueError(f"Stat {stat_name} not implemented")

    expected_lbl = ["expected_P", "expected_N"] if expected_lbl is None else expected_lbl
    tot = x[x[cm_id].isin(expected_lbl)][output_val].sum()
    stat = x[x[cm_id] == stat_name][output_val].sum()
    return pd.DataFrame({cm_id: stat_name, output_val: [stat/tot]})

def box_maximum(values: List[float]) -> float:
    """box_maximum.

    boxplot "maximum" value for the list given

    The value is equal to Q3 + 1.5 * IQR

    Parameters
    ----------
    values : List[float]
        The input values

    Returns
    -------
    float
    """
    q1 = pd.Series(values).quantile(0.25)
    q3 = pd.Series(values).quantile(0.75)
    iqr = q3 - q1
    return q3 + 1.5*iqr

@data_op
def dst_aggregate(df: pd.DataFrame,
                  cm_id: str = "cm",
                  technique: str = "dst",
                  new_clm: str = "new_clm") -> pd.DataFrame:
    """dst_aggregate.

    Aggregate the DST data.

    Parameters
    ----------
    df : pd.DataFrame
        The input data
    cm_id : str
        The column name for the aggregated statistics
    technique : str
        The technique to use for the aggregation
    new_clm : str
        The new column name

    Returns
    -------
    pd.DataFrame

    Raises
    ------
    ValueError
        If the technique is not implemented
    """
    values = df[cm_id].values
    match technique:
        case 'box_maximum':
            return df.assign(**{new_clm: box_maximum(values)})
        case 'std':
            return df.assign(**{new_clm: pd.Series(values).mean()+pd.Series(values).std()})
        case 'double_std':
            return df.assign(**{new_clm: pd.Series(values).mean()+2*pd.Series(values).std()})
        case 'mean':
            return df.assign(**{new_clm: pd.Series(values).mean()})
        case _:
            raise ValueError(f"Technique {technique} not implemented")
