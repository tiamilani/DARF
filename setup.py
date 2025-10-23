# © 2025 Nokia
# Licensed under the BSD 3-Clause License
# SPDX-License-Identifier: BSD-3-Clause
#
# Contact: Mattia Milani (Nokia) <mattia.milani@nokia.com>

from setuptools import setup, find_packages

setup(
    name='DARF', #done
    version='0.1.0', #done
    description='Plot CLI for easy plot re/generation and data manipulation', #done
    author='Mattia Milani', #done
    author_email='mattia.milani@nokia.com', #done
    packages=find_packages(exclude=['DARF.tests*', 'ez_setup']),
    package_data={"darf": ['Conf/basic.cfg']},
    setup_requires=['pytest-runner'], #done
    tests_require=['pytest', 'pytest-cov', 'pytest-mock'], #done
    entry_points={
        'console_scripts': ["darf=darf.main:main"]
    } #done
)

