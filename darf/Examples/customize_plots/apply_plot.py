# © 2025 Nokia
# Licensed under the BSD 3-Clause License
# SPDX-License-Identifier: BSD-3-Clause
#
# Contact: Mattia Milani (Nokia) <mattia.milani@nokia.com>

"""
This module is used to descibe how to use the library to generate plots
and some of the key features of the plot package.

As the dataset manipulation is possible to automate the generation of plots.
"""

import darf as scl

# Load the dataset
flights = scl.Dataset({"origin": "Online",
                       "value": "flights"})
print(flights.data)

# Create the plot
plt_m = sc
