#!/usr/bin/env python
# Software License Agreement (GPL)
#
# \file      glob_requirements
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
from Queue import Queue

from catkin.find_in_workspaces import find_in_workspaces
from catkin_pkg.package import parse_package


CATKIN_VIRTUALENV_TAGNAME = "pip_requirements"


def parse_exported_requirements(package):
    # type: (catkin_pkg.package.Package) -> List[str]
    requirements_list = []
    for export in package.exports:
        if export.tagname == CATKIN_VIRTUALENV_TAGNAME:
            try:
                requirements_path = find_in_workspaces(
                    project=package.name,
                    path=export.content,
                    first_match_only=True,
                )[0]
            except:
                print("Package {package} declares <{tagname}> {file}, which cannot be found in the package".format(
                    package=package.name, tagname=CATKIN_VIRTUALENV_TAGNAME, file=export.content), file=sys.stderr)
            else:
                requirements_list.append(requirements_path)
    return requirements_list


def process_package(package_name, soft_fail=True):
    # type: (str) -> List[str], List[str]
    try:
        package_path = find_in_workspaces(
            project=package_name,
            path="package.xml",
            first_match_only=True,
        )[0]
    except IndexError:
        if not soft_fail:
            raise RuntimeError("Unable to process package {}".format(package_name))
        else:
            # This is not a catkin dependency
            return [], []
    else:
        package = parse_package(package_path)
        dependencies = package.build_depends + package.exec_depends + package.test_depends
        return parse_exported_requirements(package), dependencies


def glob_requirements(package_name, no_deps):
    # type: (str) -> int
    package_queue = Queue()
    package_queue.put(package_name)
    processed_packages = set()
    requirements_list = []

    while not package_queue.empty():
        queued_package = package_queue.get()

        if queued_package not in processed_packages:
            processed_packages.add(queued_package)
            requirements, dependencies = process_package(
                package_name=queued_package, soft_fail=(queued_package != package_name))
            requirements_list = requirements_list + requirements

            if not no_deps:
                for dependency in dependencies:
                    package_queue.put(dependency.name)

    print(';'.join(requirements_list))
    return 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--package-name', type=str, required=True)
    parser.add_argument('--no-deps', action="store_true")
    args, unknown = parser.parse_known_args()

    sys.exit(glob_requirements(**vars(args)))
