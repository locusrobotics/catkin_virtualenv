#!/usr/bin/env python
# Software License Agreement (GPL)
#
# \file      venv.py
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
import logging
import re
import shutil
import subprocess

from distutils.spawn import find_executable

from . import check_call, relocate
from .collect_requirements import collect_requirements

_BYTECODE_REGEX = re.compile('.*.py[co]')

logger = logging.getLogger(__name__)


class Virtualenv:

    def __init__(self, path):
        """ Manage a virtualenv at the specified path. """
        self.path = path

    def initialize(self, python, use_system_packages, extra_pip_args, clean=True):
        """ Initialize a new virtualenv using the specified python version and extra arguments. """
        if clean:
            try:
                shutil.rmtree(self.path)
            except:
                pass

        system_python = find_executable(python)

        if not system_python:
            raise RuntimeError("Unable to find a system-installed {}".format(python))

        preinstall = [
            "pip==20.1",
            "pip-tools==5.1.2",
        ]

        builtin_venv = self._check_module(system_python, 'venv')
        if builtin_venv:
            virtualenv = [system_python, '-m', 'venv']
        else:
            virtualenv = [
                'virtualenv',
                '--no-setuptools',
                '--verbose',
                '--python', python
            ]
            # py2's virtualenv command will try install latest setuptools. setuptools>=45 not compatible with py2
            preinstall += ['setuptools<45']

        if use_system_packages:
            virtualenv.append('--system-site-packages')

        virtualenv.append(self.path)
        check_call(virtualenv)

        venv_python = self._venv_bin('python')

        builtin_pip = self._check_module(venv_python, 'pip')
        if builtin_pip:
            pip_tool = [venv_python, '-m', 'pip']
        else:
            pip_tool = [self._venv_bin('pip')]

        pip_args = ['install'] + extra_pip_args

        check_call(pip_tool + pip_args + preinstall)

    def sync(self, requirements, extra_pip_args):
        """ Sync a virtualenv with the specified requirements. """
        pip_sync = self._venv_bin('pip-sync')
        command = [pip_sync, requirements]

        if extra_pip_args:
            command += ['--pip-args', "\'" + ' '.join(extra_pip_args) + "\'"]

        check_call(command)

    def freeze(self, package_name, output_requirements, no_deps, no_overwrite, extra_pip_args):
        """ Create a frozen requirement set from a set of input specifications. """
        if no_overwrite and os.path.exists(output_requirements):
            logger.info("Lock file already exists, not overwriting")
            return

        pip_compile = self._venv_bin('pip-compile')
        command = [pip_compile]

        input_requirements = collect_requirements(package_name, no_deps)
        command += input_requirements

        if os.path.normpath(output_requirements) in input_requirements:
            raise RuntimeError("Trying to write locked requirements {} into a path specified as input: {}".format(
                output_requirements, input_requirements)
            )

        if extra_pip_args:
            command += ['--pip-args', "\'" + ' '.join(extra_pip_args) + "\'"]

        command += ['-o', output_requirements]

        check_call(command)
        logger.info("Wrote new lock file to {}".format(output_requirements))

    def relocate(self, target_dir):
        """ Relocate a virtualenv to another directory. """
        self._delete_bytecode()
        relocate.fix_shebangs(self.path, target_dir)
        relocate.fix_activate_path(self.path, target_dir)

        # This workaround has been flaky - let's just delete the 'local' folder entirely
        # relocate.fix_local_symlinks(self.path)
        local_dir = os.path.join(self.path, 'local')
        if os.path.exists(local_dir):
            shutil.rmtree(local_dir)

    def _venv_bin(self, binary_name):
        return os.path.abspath(os.path.join(self.path, 'bin', binary_name))

    def _check_module(self,  python_executable, module):
        try:
            with open(os.devnull, 'w') as devnull:
                # "-c 'import venv'" does not work with the subprocess module, but '-cimport venv' does
                check_call([python_executable, '-cimport {}'.format(module)], stderr=devnull)
            return True
        except subprocess.CalledProcessError:
            return False

    def _delete_bytecode(self):
        """ Remove all .py[co] files since they embed absolute paths. """
        for root, _, files in os.walk(self.path):
            for f in files:
                if _BYTECODE_REGEX.match(f):
                    os.remove(os.path.join(root, f))
