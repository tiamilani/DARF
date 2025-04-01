# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright (C) 2021 Mattia Milani <mattia.milani@nokia.com>

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

