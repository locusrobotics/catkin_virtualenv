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
import re
import sys

from collections import namedtuple
from packaging.requirements import Requirement

comment_regex = re.compile(r'\s*#.*')

CombinedRequirement = namedtuple("CombinedRequirement", "requirement source suppressed_set")
SuppressedRequirement = namedtuple("SuppressedRequirement", "requirement source")


def combine_requirements(requirements_list, output_file):
    # type: (List[IO], IO) -> int
    combined_requirements = {}  # type: Dict[str, requirements.Requirement]
    for requirements_file in requirements_list:
        contents = requirements_file.read()
        contents = comment_regex.sub('', contents)
        for requirement_string in contents.splitlines():
            if requirement_string and not requirement_string.isspace():
                requirement = Requirement(requirement_string)
                if requirement.name not in combined_requirements:
                    combined_requirements[requirement.name] = CombinedRequirement(
                        requirement=requirement,
                        source=requirements_file.name,
                        suppressed_set=set()
                    )
                else:
                    combined_requirements[requirement.name].suppressed_set.add(
                        SuppressedRequirement(
                            requirement=requirement,
                            source=requirements_file.name)
                        )

    for entry in combined_requirements.values():
        output_file.write("{} # from {}\n".format(entry.requirement, entry.source))
        for suppressed in entry.suppressed_set:
            output_file.write("# suppressed {} from {}\n".format(suppressed.requirement, suppressed.source))

    return 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--requirements-list', type=argparse.FileType('r'), nargs='*', required=True)
    parser.add_argument('--output-file', type=argparse.FileType('w'), required=True)
    args, unknown = parser.parse_known_args()

    sys.exit(combine_requirements(**vars(args)))
