#!/usr/bin/env python
# Software License Agreement (GPL)
#
# \file      build_venv
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
import os
import re
import shutil
import sys

from dh_virtualenv import Deployment
from distutils.spawn import find_executable


_BYTECODE_REGEX = re.compile('.*.py[co]')


def delete_bytecode(directory):
    for root, dirs, files in os.walk(directory):
        for f in files:
            if _BYTECODE_REGEX.match(f):
                os.remove(os.path.join(root, f))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Build a virtualenv, and rewrite the internal paths with an arbitrary root directory.")
    parser.add_argument(
        '--requirements', required=True, help="A requirements.txt file specifying dependencies.")
    parser.add_argument(
        '--root-dir', required=True, help="Directory to which the virtualenv's hardcoded paths should be rewritten.")
    parser.add_argument(
        '--python3', action='store_true', help="Build the virtualenv with Python3 as the default interpreter.")

    args, unknown = parser.parse_known_args()

    root_dir = os.path.realpath(args.root_dir)

    os.environ['DH_VIRTUALENV_INSTALL_ROOT'] = os.path.dirname(root_dir)

    deploy = Deployment(
        package=os.path.basename(root_dir),
        requirements_filename=args.requirements,
        upgrade_pip=True,
        verbose=False,
        use_system_packages=True,
        python=find_executable('python3') if args.python3 else find_executable('python2'),
        # TODO(pbovbel) Builtin venv (python3-venv) is not available on trusty. This flag can be re-enabled when
        # trusty support is dropped.
        # builtin_venv=args.python3,
    )

    print('Generating virtualenv in {}'.format(deploy.package_dir))
    deploy.create_virtualenv()

    print('Installing requirements')
    deploy.install_dependencies()

    print('Fixing virtualenv root to {}'.format(deploy.virtualenv_install_dir))
    deploy.fix_activate_path()
    deploy.fix_shebangs()
    deploy.fix_local_symlinks()

    # Remove all .py[co] files since they embed absolute paths
    delete_bytecode(deploy.package_dir)

    if not args.python3:
        # Remove local folder
        shutil.rmtree(os.path.join(deploy.package_dir, 'local'))

    sys.exit(0)
