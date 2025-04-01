# © 2025 Nokia
# Licensed under the BSD 3-Clause License
# SPDX-License-Identifier: BSD-3-Clause
#
# Contact: Mattia Milani (Nokia) <mattia.milani@nokia.com>

"""
This module is used to descibe how to use the library to generate the first
plot. It is a simple example that uses an online dataset, it plots and save
the output in a file.

Import libraries
----------------

The classes used in this tutorial are the baseline for every complex
system that you are going to see in more complex examples.

.. code-block:: python

        from darf.src import Dataset
        from darf.src.plot import Plotter

The first class is the Dataset class that is used to load the data from
different sources.
The second class is the Plotter class that is used to actually draw
the figure and save it in a file.

Load the dataset
----------------

The first step is to load the dataset. In this case we are going to use
the Online dataset that is a simple dataset that is loaded from the
internet. Underneath the seaborn function ``sns.load_dataset`` is used to
load the dataset. Feel free to experiment with other datasets.

.. _seaborn-load_dataset: https://seaborn.pydata.org/generated/seaborn.load_dataset.html

Refer to the seaborn-load_dataset_ documentation for more information.

.. code-block:: python

        flights = Dataset({"origin": "Online",
                           "value": "flights"})
        print(flights.data)

The first line creates the dataset object, specifing the origin: "Online"
and the value that should be used inside the ``sns.load_dataset`` function.

The dataset will be loaded in a lazy way, so the data will be effectively
downloaded and load only on the second line. where the ``print`` function
is used to show the datsaet.

The output should be something like:

.. code-block:: python

        year  month  passengers
    0    1949      1         112
    1    1949   Feb         118
    2    1949   Mar         132
    3    1949   Apr         129
    4    1949   May         121
    ..    ...   ...         ...
    139  1960   Aug         606
    140  1960   Sep         508
    141  1960   Oct         461
    142  1960   Nov         390
    143  1960   Dec         432

    [144 rows x 3 columns]

Plot the figure
---------------

The second step is to create the plot. In this case we are going to use
the Plotter class to draw a simple line plot.

.. code-block:: python

        plt = Plotter(flights.data)
        plt('line', x='year', y='passengers')
        plt.save('first_plot')

The call is used to generate the plotter object, which receives the dataset
that should be used.
The second line generates the plot, in this case a line plot, with the
x-axis being the year and the y-axis being the passengers.
The third line saves the plot in a file called ``first_plot.pdf``.
``pdf`` is the default file format used by the library.
But multiple file format could be used like ``['png', 'pdf']``, this would
generate two files with the same plot.
Please refer to the plotter module for more information.
"""

from darf.src import Dataset
from darf.src.plot import Plotter

# Load the dataset
flights = Dataset({"origin": "Online",
                   "value": "flights"})
print(flights.data)

# Create the plot
plt = Plotter(flights.data)
plt('line', x='year', y='passengers')
plt.save('first_plot')
