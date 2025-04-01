# © 2025 Nokia
# Licensed under the BSD 3-Clause License
# SPDX-License-Identifier: BSD-3-Clause
#
# Contact: Mattia Milani (Nokia) <mattia.milani@nokia.com>

"""
This example describe how to use operations in order to manipulate the dataset
loaded.

Operations are functions calls that can be predefined by the user to later
be used to manipulate the dataset.

In order to use operations it's requried to import the ``Operations`` class.

.. code-block:: python

        from darf import Operations

This class contains the method to create and manage operations.

It's possible to create easily one operation using the ``Operations.one`` method.

.. code-block:: python

        op = Operations.one("rename_dec", "rename_val", old_val=['Dec'], new_val=['December'])

The First argument is the name of the operation, the second is the function to call.
What follows are the arguments to pass to the function.

This operation can be applied to the dataset using the ``operations`` parameter
when creating the dataset as follows:

.. code-block:: python

            # Load the dataset
            flights = Dataset({"origin": "Online",
                               "value": "flights",
                               "operations": ['rename_dec']},
                              operations=op)

The op passed to the datasaet class can contain multiple functions to apply
to different datasets. Each dataset should specify the list of operations
that should be applied to it using the "operations" keyword in the dataset
definition.

Another way to create operations is to use directly the ``Operations`` class directly.
But this is thought to be used when multiple operations are needed and with
function that takes care about foramtting properly the argument dictionary.

An example is as follows:

.. code-block:: python

            op = Operations({"rename_dec": {"value": "rename_val",
                                            "kwargs": {"old_val": ['Dec'],
                                                    "new_val": ['December']}
                                            },
                            "drop_nov": {"value": "drop_row",
                                        "kwargs": {"clm": 'month',
                                                    "val": 'Nov'}
                                        }
                            })

A more simpler approach when defining multiple operations is to use the
concat method of the Operations class.

.. code-block:: python

            op1 = Operations.one("rename_dec", "rename_val", old_val=['Dec'], new_val=['December'])
            op2 = Operations.one("drop_nov", "drop_row", clm='month', val='Nov')
            ops = Operations.concat(op1, op2)
"""

from darf import Dataset, Operations

# Load the dataset
flights = Dataset({"origin": "Online",
                   "value": "flights"})

op = Operations.one("rename_dec", "rename_val", old_val=['Dec'], new_val=['December'])

# Load the dataset
flights = Dataset({"origin": "Online",
                   "value": "flights",
                   "operations": ['rename_dec']},
                  operations=op)
print(flights.data)

op = Operations({"rename_dec": {"value": "rename_val",
                                "kwargs": {"old_val": ['Dec'],
                                           "new_val": ['December']}
                                },
                 "drop_nov": {"value": "drop_row",
                              "kwargs": {"clm": 'month',
                                         "val": 'Nov'}
                              }
                 })

# Load the dataset
flights = Dataset({"origin": "Online",
                   "value": "flights",
                   "operations": ['rename_dec', 'drop_nov']},
                  operations=op)
print(flights.data)

op1 = Operations.one("rename_dec", "rename_val", old_val=['Dec'], new_val=['December'])
op2 = Operations.one("drop_nov", "drop_row", clm='month', val='Nov')
ops = Operations.concat(op1, op2)
print(ops)
