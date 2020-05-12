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

from .collect_requirements import collect_requirements

_BYTECODE_REGEX = re.compile('.*.py[co]')

PYTHON_INTERPRETERS = ['python', 'pypy', 'ipy', 'jython']
_PYTHON_INTERPRETERS_REGEX = r'\(' + r'\|'.join(PYTHON_INTERPRETERS) + r'\)'

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
        subprocess.check_call(virtualenv)

        venv_python = self._venv_bin('python')

        builtin_pip = self._check_module(venv_python, 'pip')
        if builtin_pip:
            pip_tool = [venv_python, '-m', 'pip']
        else:
            pip_tool = [self._venv_bin('pip')]

        pip_args = ['install'] + extra_pip_args

        subprocess.check_call(pip_tool + pip_args + preinstall)

    def sync(self, requirements, extra_pip_args):
        """ Sync a virtualenv with the specified requirements. """
        pip_sync = self._venv_bin('pip-sync')
        command = [pip_sync, requirements]

        if extra_pip_args:
            command += ['--pip-args', "\'" +' '.join(extra_pip_args) + "\'"]

        subprocess.check_call(command)

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
            command += ['--pip-args', "\'" +' '.join(extra_pip_args) + "\'"]

        command += ['-o', output_requirements]

        logger.info("Writing new lock file")
        logger.info(command)
        subprocess.check_call(command)

    def relocate(self, target_dir):
        """ Relocate a virtualenv to another directory. """
        self._delete_bytecode()
        self._fix_shebangs(target_dir)
        self._fix_activate_path(target_dir)

        # This workaround has been flaky - let's just delete the 'local' folder entirely
        # self._fix_local_symlinks()
        local_dir = os.path.join(self.path, 'local')
        if os.path.exists(local_dir):
            # Remove local folder
            shutil.rmtree(local_dir)

    def _venv_bin(self, binary_name):
        return os.path.abspath(os.path.join(self.path, 'bin', binary_name))

    def _check_module(self,  python_executable, module):
        try:
            with open(os.devnull, 'w') as devnull:
                # "-c 'import venv'" does not work with the subprocess module, but '-cimport venv' does
                subprocess.check_call([python_executable, '-cimport {}'.format(module)], stderr=devnull)
            return True
        except subprocess.CalledProcessError:
            return False

    def _delete_bytecode(self):
        """ Remove all .py[co] files since they embed absolute paths. """
        for root, _, files in os.walk(self.path):
            for f in files:
                if _BYTECODE_REGEX.match(f):
                    os.remove(os.path.join(root, f))

    def _find_script_files(self):
        """Find list of files containing python shebangs in the bin directory. """
        command = ['grep', '-l', '-r',
                   '-e', r'^#!.*bin/\(env \)\?{0}'.format(_PYTHON_INTERPRETERS_REGEX),
                   '-e', r"^'''exec.*bin/{0}".format(_PYTHON_INTERPRETERS_REGEX),
                   os.path.join(self.path, 'bin')]
        grep_proc = subprocess.Popen(command, stdout=subprocess.PIPE)
        files, stderr = grep_proc.communicate()
        return set(f for f in files.decode('utf-8').strip().split('\n') if f)

    def _fix_shebangs(self, target_dir):
        """Translate /usr/bin/python and /usr/bin/env python shebang
        lines to point to our virtualenv python.
        """
        pythonpath = os.path.join(target_dir, 'bin/python')
        for f in self._find_script_files():
            regex = (
                r's-^#!.*bin/\(env \)\?{names}\"\?-#!{pythonpath}-;'
                r"s-^'''exec'.*bin/{names}-'''exec' {pythonpath}-"
            ).format(names=_PYTHON_INTERPRETERS_REGEX, pythonpath=re.escape(pythonpath))
            subprocess.check_call(['sed', '-i', regex, f])

    def _fix_activate_path(self, target_dir):
        """Replace the `VIRTUAL_ENV` path in bin/activate to reflect the
        post-install path of the virtualenv.
        """
        activate_settings = [
            [
                'VIRTUAL_ENV="{0}"'.format(target_dir),
                r'^VIRTUAL_ENV=.*$',
                "activate"
            ],
            [
                'setenv VIRTUAL_ENV "{0}"'.format(target_dir),
                r'^setenv VIRTUAL_ENV.*$',
                "activate.csh"
            ],
            [
                'set -gx VIRTUAL_ENV "{0}"'.format(target_dir),
                r'^set -gx VIRTUAL_ENV.*$',
                "activate.fish"
            ],
        ]

        for activate_args in activate_settings:
            virtualenv_path = activate_args[0]
            pattern = re.compile(activate_args[1], flags=re.M)
            activate_file = activate_args[2]

            with open(self._venv_bin(activate_file), 'r+') as fh:
                content = pattern.sub(virtualenv_path, fh.read())
                fh.seek(0)
                fh.truncate()
                fh.write(content)

    def _fix_local_symlinks(self):
        # The virtualenv might end up with a local folder that points outside the package
        # Specifically it might point at the build environment that created it!
        # Make those links relative
        # See https://github.com/pypa/virtualenv/commit/5cb7cd652953441a6696c15bdac3c4f9746dfaa1
        local_dir = os.path.join(self.path, "local")
        if not os.path.isdir(local_dir):
            return
        elif os.path.samefile(self.path, local_dir):
            # "local" points directly to its containing directory
            os.unlink(local_dir)
            os.symlink(".", local_dir)
            return

        for d in os.listdir(local_dir):
            path = os.path.join(local_dir, d)
            if not os.path.islink(path):
                continue

            existing_target = os.readlink(path)
            if not os.path.isabs(existing_target):
                # If the symlink is already relative, we don't
                # want to touch it.
                continue

            new_target = os.path.relpath(existing_target, local_dir)
            os.unlink(path)
            os.symlink(new_target, path)
