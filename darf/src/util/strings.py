# © 2025 Nokia
# Licensed under the BSD 3-Clause License
# SPDX-License-Identifier: BSD-3-Clause
#
# Contact: Mattia Milani (Nokia) <mattia.milani@nokia.com>

"""
strings module
==============

Module used to control in one place all the strings of the program

"""


class s: # pylint: disable=too-few-public-methods,unused-variable
    """s.

    Class used to manage strings in the program
    """

    # Helpers
    verbose_help = "Define the level of verbosity in the logs"
    silent_help = "Flag to deactivate the output to the STDOUT"
    csv_help = "Flag to activate the csv output style"

    # default conf
    default_conf = "default_ini"

    # IO keys
    io_name_key = "name"
    io_type_key = "type"
    io_subtype_key = "subtype"
    io_path_key = "path"
    io_exists_key = "exists"

    # Types of IO objects
    folder_obj_types = ["folder", "direcotry"]
    file_obj_types = ["file"]
    remote_obj_types = ["remote"]
    local_path_key = "local"
    io_types = folder_obj_types + file_obj_types + remote_obj_types
    dataset_obj_type = "dataset"
    dataset_obj_types = ["dataset"]
    data_operations_key = "operations"
    plot_operations_key = "operations"
    sub_obj_type = ["input_data"]
    param_depends_on_key = "depends_on"

    # Data objects
    data_key = "data"
    data_origin_key = "origin"
    dst_origin_depends_on = ["Copy", "Dependent", "Join"]
    all_dst_origin = dst_origin_depends_on + ["Local", "CsvPkl", "TfPkl", "TfPklList",
                                              "TfPklListIterator", "Online",
                                              "ObjPklList", "Remote"]

    # General data container
    input_data = "input_data"

    # Results containers
    results_path = "output_path"

    # Pkl containers
    pkl_path = "pkl_path"

    # Logs
    log_path = "log_path"
    log_file = "log_file"

    # Environment parameters
    param_value = "value"
    param_generic_type = "generic"
    param_op_type = "operation"
    param_plot_op_type = "plot_operation"
    param_dataset_type = "dataset"
    param_action_args = "args"
    param_action_kwargs = "kwargs"
    param_plot_type = "plot"
    param_types = [param_generic_type, param_op_type, param_plot_op_type, dataset_obj_type]
    param_args_ast = [param_plot_type, param_op_type, param_dataset_type, param_plot_op_type]
    env_par = "environment"
    numpy_rng = "numpy_rng"
    env_rng = "rng"
    env_tf_rng = "tf_rng"

    # Plot conf
    plot_datasets_key = "dataset"
    plot_extensions_key = "extension"
    plot_output_name_key = "output_name"
    plot_set_kwargs_key = "set_kwargs"
    plot_set_special_key = "set_special"
    plot_set_legend_key = "set_legend"
    plot_dataset_keywords_key = "dataset_keywords"
    plot_dataset_keywords_col_id = "col_id"
    plot_dataset_keywords_values = "value"
    plot_regenerate_key = "regenerate"
    plot_legend_key = "legend_flag"
    plot_key = "plot_conf"
    plot_format = "plot_format"
    plot_features = "plot_features"
    plot_palette_key = "palette"
    plot_special_legend_key = "special_legend"
    plot_dataset_merge_axis_key = "merge_axis"
    network_plot_features = "network_plot_features"
    history_xlim = "history_xlim"
    history_ylim = "history_ylim"

    # Log utils
    log_format = "%(asctime)s - %(levelname)s - %(message)s"

    # Pkl save
    group_df_pkl = "groups_df"
    last_layer_test = "tsne-resulting-df-{}"

    appendix_key = "appendix"
