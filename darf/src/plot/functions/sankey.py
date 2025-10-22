# © 2025 Nokia
# Licensed under the BSD 3-Clause License
# SPDX-License-Identifier: BSD-3-Clause
#
# Contact: Mattia Milani (Nokia) <mattia.milani@nokia.com>

from typing import Optional, List, Union
import pandas as pd
import seaborn as sns
import matplotlib as mplt
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
from matplotlib.path import Path
from matplotlib.patches import PathPatch
from darf.src.decorators.decorators import plot

@plot
def sankey(data: Optional[pd.DataFrame] = None,
           classes: List[str] = ["G", "B", "U"],
           class_colors = ["#4daf4a", "#377eb8", "#e41a1c"],
           source_clm: str = "source",
           source_class_clm: str = "source_class",
           target_clm: str = "target",
           target_class_clm: str = "target_class",
           value_clm: str = "value",
           it_clm: str = "Iteration",
           **kwargs) -> plt.Axes:
    """sankey.

    Plot a sankey diagram with the data provided.

    Parameters
    ----------
    data : pd.DataFrame
        The input data
    classes : List[str]
        List of classes to be used in the sankey diagram
    class_colors : List[str]
        List of colors to be used for each class
    source_clm : str
        The column name of the source column
    source_class_clm : str
        The column name of the source class column, used to color the source
    target_clm : str
        The column name of the target column
    target_class_clm : str
        The column name of the target class column, used to color the target
    value_clm : str
        The column name of the value column, used to identify the width of the lines
    it_clm : str
        The column name of the iteration column

    returns
    -------
    mplt.axes.Axes
        The axes of the plot
    """
    if data is None or data.empty:
        raise ValueError("No data provided for the Sankey diagram")

    # Setup the figure and axis
    fig, ax = plt.subplots(figsize=(12, 8))

    # Remove grid and borders
    ax.grid(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)

    # Get unique iterations
    if it_clm not in data.columns:
        raise ValueError(f"Iteration column '{it_clm}' not found in the data")

    iterations = sorted(data[it_clm].unique())

    # Set the x positions for the iterations
    x_positions = {it: i for i, it in enumerate(iterations)}

    # Collect all unique nodes (sources and targets)
    all_nodes = set(data[source_clm].unique()) | set(data[target_clm].unique())

    # Create a mapping for node vertical positions
    node_positions = {}
    node_heights = {}

    # Calculate block heights for each node at each iteration
    for it in iterations:
        it_data = data[data[it_clm] == it]

        # For sources in this iteration
        for node in it_data[source_clm].unique():
            if it == iterations[0]:  # First iteration
                # Sum of outgoing flow
                flow = it_data[it_data[source_clm] == node][value_clm].sum()
                node_heights[(node, it)] = flow
            else:
                # Get the previous heights if available
                node_heights[(node, it)] = node_heights.get((node, it-1), 0)

        # For targets in this iteration
        for node in it_data[target_clm].unique():
            # Sum of incoming flow
            flow = it_data[it_data[target_clm] == node][value_clm].sum()
            node_heights[(node, it)] = flow

    # Normalize heights for better visualization
    max_height = max(node_heights.values()) if node_heights else 1
    scale_factor = 0.8 / max_height  # 80% of the plot height

    # Calculate y positions for blocks
    y_offset = 0.1  # Starting from 10% from the bottom

    # Group nodes by iteration for vertical positioning
    for it in iterations:
        # Get nodes in this iteration
        it_sources = set(data[data[it_clm] == it][source_clm].unique())
        it_targets = set(data[data[it_clm] == it][target_clm].unique())
        it_nodes = it_sources | it_targets

        # Calculate total height needed for this iteration
        total_height = sum(node_heights.get((node, it), 0) for node in it_nodes)
        current_y = y_offset

        # Position each node
        for node in sorted(it_nodes):
            height = node_heights.get((node, it), 0) * scale_factor
            if height > 0:
                node_positions[(node, it)] = current_y + height / 2
                current_y += height + 0.02  # Add a small gap between blocks

    # Draw blocks for each node at each iteration
    block_width = 0.2  # Define block_width here so it's accessible throughout the function
    for (node, it), y_center in node_positions.items():
        x_pos = x_positions[it]
        height = node_heights[(node, it)] * scale_factor

        # Determine if this is a source or target at this iteration
        is_source = node in data[(data[it_clm] == it) & (data[source_clm] == node)][source_clm].values
        is_target = node in data[(data[it_clm] == it) & (data[target_clm] == node)][target_clm].values

        # Determine color based on class
        if is_source and source_class_clm in data.columns:
            # Get most common class for this node as source
            node_class = data[(data[it_clm] == it) & (data[source_clm] == node)][source_class_clm].mode()[0]
        elif is_target and target_class_clm in data.columns:
            # Get most common class for this node as target
            node_class = data[(data[it_clm] == it) & (data[target_clm] == node)][target_class_clm].mode()[0]
        else:
            node_class = None

        # Set color based on class
        if node_class in classes:
            color = class_colors[classes.index(node_class)]
        else:
            color = "#cccccc"  # Default gray

        # Draw rectangle
        block_width = 0.2
        rect = Rectangle((x_pos - block_width/2, y_center - height/2),
                         block_width, height,
                         facecolor=color, alpha=0.7, edgecolor='black')
        ax.add_patch(rect)

        # Only add node labels outside the blocks
        ax.text(x_pos, y_center + height/2 + 0.01, node, ha='center', va='bottom',
                fontsize=8, rotation=45)

    # Draw flows between blocks
    for _, row in data.iterrows():
        source = row[source_clm]
        target = row[target_clm]
        value = row[value_clm]
        it = row[it_clm]

        # Skip if we don't have target iteration data
        if it == iterations[-1]:
            continue

        next_it = iterations[iterations.index(it) + 1]

        # Get source and target positions
        source_x = x_positions[it]
        source_y = node_positions.get((source, it))
        target_x = x_positions[next_it]
        target_y = node_positions.get((target, next_it))

        if source_y is None or target_y is None:
            continue

        # Calculate flow width based on value and proportions
        source_total = data[(data[it_clm] == it) & (data[source_clm] == source)][value_clm].sum()
        target_total = data[(data[it_clm] == next_it) & (data[target_clm] == target)][value_clm].sum()

        # Width at source is proportional to value/source_total
        source_width_ratio = value / source_total if source_total > 0 else 0
        # Width at target is proportional to value/target_total
        target_width_ratio = value / target_total if target_total > 0 else 0

        # Calculate actual widths (scaled to the height of the blocks)
        source_width = source_width_ratio * node_heights[(source, it)] * scale_factor
        target_width = target_width_ratio * node_heights[(target, next_it)] * scale_factor

        # Determine color based on source class
        if source_class_clm in data.columns:
            source_class = row[source_class_clm]
            if source_class in classes:
                color = class_colors[classes.index(source_class)]
            else:
                color = "#cccccc"
        else:
            color = "#cccccc"

        # Create a curved path between source and target
        # Control points for a nice curve
        control1_x = source_x + (target_x - source_x) * 0.4
        control2_x = source_x + (target_x - source_x) * 0.6

        # Create a path with variable width
        # Since matplotlib doesn't support variable width paths directly,
        # we'll draw multiple thin paths to approximate the tapered effect
        num_segments = 10
        for i in range(num_segments):
            # Calculate the vertical offsets for this segment
            # Start narrow at source and widen at target (or vice versa)
            source_offset = source_width / 2 * (i / (num_segments - 1) - 0.5) * 2
            target_offset = target_width / 2 * (i / (num_segments - 1) - 0.5) * 2

            verts = [
                (source_x + block_width/2, source_y + source_offset),  # start
                (control1_x, source_y + source_offset * 0.7),         # control 1
                (control2_x, target_y + target_offset * 0.7),         # control 2
                (target_x - block_width/2, target_y + target_offset)  # end
            ]

            codes = [
                Path.MOVETO,
                Path.CURVE4,
                Path.CURVE4,
                Path.CURVE4
            ]

            # Create and add the path
            path = Path(verts, codes)
            patch = PathPatch(path, facecolor='none', edgecolor=color,
                            linewidth=1, alpha=0.4)
            ax.add_patch(patch)

    # Set x-axis ticks to show iterations
    ax.set_xticks(list(x_positions.values()))
    ax.set_xticklabels([f"Iteration {it}" for it in iterations])

    # Hide y-axis ticks
    ax.set_yticks([])

    # Set axis limits
    ax.set_xlim(-0.5, len(iterations) - 0.5)
    ax.set_ylim(0, 1)

    # Add legend for classes
    legend_elements = [Rectangle((0, 0), 1, 1, facecolor=class_colors[i], label=cls)
                      for i, cls in enumerate(classes) if i < len(class_colors)]
    ax.legend(handles=legend_elements, loc='upper right')

    # Make sure the plot fits well
    plt.tight_layout()

    plt.show()
    raise Exception("Sankey diagram not implemented yet")

    # Return the axes object
    return ax
