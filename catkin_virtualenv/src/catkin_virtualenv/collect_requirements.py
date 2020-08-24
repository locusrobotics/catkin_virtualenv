#!/usr/bin/env python
# Software License Agreement (GPL)
#
# \file      collect_requirements.py
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

import os

from queue import Queue
from catkin.find_in_workspaces import find_in_workspaces
from catkin_pkg.package import parse_package


CATKIN_VIRTUALENV_TAGNAME = "pip_requirements"


def parse_exported_requirements(package, package_dir):
    # type: (catkin_pkg.package.Package) -> List[str]
    requirements_list = []
    for export in package.exports:
        if export.tagname == CATKIN_VIRTUALENV_TAGNAME:
            requirements_list.append(os.path.join(package_dir, export.content))
    return requirements_list


def process_package(package_name, soft_fail=True):
    # type: (str) -> List[str], List[str]
    try:
        package_path = find_in_workspaces(project=package_name, path="package.xml", first_match_only=True,)[0]
    except IndexError:
        if not soft_fail:
            raise RuntimeError("Unable to process package {}".format(package_name))
        else:
            # This is not a catkin dependency
            return [], []
    else:
        package = parse_package(package_path)
        dependencies = package.build_depends + package.test_depends
        return parse_exported_requirements(package, os.path.dirname(package_path)), dependencies


def collect_requirements(package_name, no_deps=False):
    # type: (str, bool) -> List[str]
    """ Collect requirements inherited by a package. """
    package_queue = Queue()
    package_queue.put(package_name)
    processed_packages = set()
    requirements_list = []

    while not package_queue.empty():
        queued_package = package_queue.get()

        if queued_package not in processed_packages:
            processed_packages.add(queued_package)
            requirements, dependencies = process_package(
                package_name=queued_package, soft_fail=(queued_package != package_name)
            )
            requirements_list = requirements + requirements_list

            if not no_deps:
                for dependency in dependencies:
                    package_queue.put(dependency.name)

    return requirements_list
