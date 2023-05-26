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

import difflib
import logging
import os
import re
import shutil
import subprocess
import tempfile
try:
    from urllib.request import urlretrieve
except ImportError:
    # for python2
    from urllib import urlretrieve

from distutils.spawn import find_executable

from . import run_command, relocate
from .collect_requirements import collect_requirements

_BYTECODE_REGEX = re.compile(r".*\.py[co]")
_COMMENT_REGEX = re.compile(r"(^|\s+)#.*$", flags=re.MULTILINE)

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
            except Exception:
                pass

        system_python = find_executable(python)

        if not system_python:
            error_msg = "Unable to find a system-installed {}.".format(python)
            if python and python[0].isdigit():
                error_msg += " Perhaps you meant python{}".format(python)
            raise RuntimeError(error_msg)

        preinstall = [
            "pip==22.0.2",
            "pip-tools==6.10.0",
        ]

        builtin_venv = self._check_module(system_python, "venv")
        if builtin_venv:
            virtualenv = [system_python, "-m", "venv"]
        else:
            virtualenv = ["virtualenv", "--no-setuptools", "--verbose", "--python", python]
            # py2's virtualenv command will try install latest setuptools. setuptools>=45 not compatible with py2,
            # but we do require a reasonably up-to-date version (because of pip==20.1), so v44 at least.
            preinstall += ["setuptools>=44,<45"]

        if use_system_packages:
            virtualenv.append("--system-site-packages")

        without_pip = self._check_module(system_python, "ensurepip") is False
        if without_pip:
            virtualenv.append('--without-pip')

        virtualenv.append(self.path)
        run_command(virtualenv, check=True)

        if without_pip:
            # install pip via get-pip.py
            version_proc = run_command(
                ['python', "-cimport sys; print('{}.{}'.format(*sys.version_info))"],
                capture_output=True)
            version = version_proc.stdout
            if isinstance(version, bytes):
                version = version.decode('utf-8')
            version = version.strip()
            # download pip from https://bootstrap.pypa.io/pip/
            get_pip_path, _ = urlretrieve("https://bootstrap.pypa.io/pip/get-pip.py")
            run_command([self._venv_bin("python"), get_pip_path], check=True)

        run_command([self._venv_bin("python"), "-m", "pip", "install"] + extra_pip_args + preinstall, check=True)

    def install(self, requirements, extra_pip_args):
        """ Sync a virtualenv with the specified requirements. """
        command = [self._venv_bin("python"), "-m", "pip", "install"] + extra_pip_args
        for req in requirements:
            run_command(command + ["-r", req], check=True)

    def check(self, requirements, extra_pip_args):
        """ Check if a set of requirements is completely locked. """
        with open(requirements, "r") as f:
            existing_requirements = f.read()

        # Re-lock the requirements
        command = [self._venv_bin("pip-compile"), "--no-header", "--annotation-style", "line", requirements, "-o", "-"]
        if extra_pip_args:
            command += ["--pip-args", " ".join(extra_pip_args)]

        generated_requirements = run_command(command, check=True, capture_output=True).stdout.decode()

        def _format(content):
            # Remove comments
            content = _COMMENT_REGEX.sub("", content)
            # Remove case sensitivity
            content = content.lower()
            # Split into lines for diff
            content = content.splitlines()
            # ignore order
            content.sort()
            return content

        # Compare against existing requirements
        diff = list(difflib.unified_diff(_format(existing_requirements), _format(generated_requirements)))

        return diff

    def lock(self, package_name, input_requirements, no_overwrite, extra_pip_args):
        """ Create a frozen requirement set from a set of input specifications. """
        try:
            output_requirements = collect_requirements(package_name, no_deps=True)[0]
        except IndexError:
            logger.info("Package doesn't export any requirements, step can be skipped")
            return

        if no_overwrite and os.path.exists(output_requirements):
            logger.info("Lock file already exists, not overwriting")
            return

        pip_compile = self._venv_bin("pip-compile")
        command = [pip_compile, "--no-header", "--annotation-style", "line", input_requirements]

        if os.path.normpath(input_requirements) == os.path.normpath(output_requirements):
            raise RuntimeError(
                "Trying to write locked requirements {} into a path specified as input: {}".format(
                    output_requirements, input_requirements
                )
            )

        if extra_pip_args:
            command += ["--pip-args", " ".join(extra_pip_args)]

        command += ["-o", output_requirements]

        run_command(command, check=True)

        logger.info("Wrote new lock file to {}".format(output_requirements))

    def relocate(self, target_dir):
        """ Relocate a virtualenv to another directory. """
        self._delete_bytecode()
        relocate.fix_shebangs(self.path, target_dir)
        relocate.fix_activate_path(self.path, target_dir)

        # This workaround has been flaky - let's just delete the 'local' folder entirely
        # relocate.fix_local_symlinks(self.path)
        local_dir = os.path.join(self.path, "local")
        if os.path.exists(local_dir):
            shutil.rmtree(local_dir)

    def _venv_bin(self, binary_name):
        if os.path.exists(os.path.join(self.path, "bin", binary_name)):
            return os.path.abspath(os.path.join(self.path, "bin", binary_name))
        elif os.path.exists(os.path.join(self.path, "local", "bin", binary_name)):
            return os.path.abspath(os.path.join(self.path, "local", "bin", binary_name))
        raise RuntimeError("Binary {} not found in venv".format(binary_name))

    def _check_module(self, python_executable, module):
        try:
            with open(os.devnull, "w") as devnull:
                # "-c 'import venv'" does not work with the subprocess module, but '-cimport venv' does
                run_command([python_executable, "-cimport {}".format(module)], stderr=devnull, check=True)
            return True
        except subprocess.CalledProcessError:
            return False

    def _delete_bytecode(self):
        """ Remove all .py[co] files since they embed absolute paths. """
        for root, _, files in os.walk(self.path):
            for f in files:
                if _BYTECODE_REGEX.match(f):
                    os.remove(os.path.join(root, f))
