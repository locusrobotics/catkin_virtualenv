#!/usr/bin/env python
# Software License Agreement (GPL)
#
# \file      combine_requirements
# \authors   Paul Bovbel <pbovbel@locusrobotics.com>
# \copyright Copyright (c) (2017,), Locus Robotics, All rights reserved.
#
# This program is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 2 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
from __future__ import print_function

import argparse
import sys


def combine_requirements(requirements_list, output_file):
    # type: (List[IO], IO) -> int
    for requirements_file in requirements_list:
        output_file.write("-r {}\n".format(requirements_file))
    return 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--requirements-list', type=str, nargs='*', required=True)
    parser.add_argument('--output-file', type=argparse.FileType('w'), required=True)
    args, unknown = parser.parse_known_args()

    sys.exit(combine_requirements(**vars(args)))
