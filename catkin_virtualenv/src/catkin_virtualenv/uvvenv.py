#!/usr/bin/env python
# Software License Agreement (GPL)
#
# \file      uvvenv.py
# \authors   Barrett Strausser <bstrausser@locusrobotics.com>
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

from .venv import Virtualenv
from .collect_requirements import collect_requirements
import pathlib
import typing
import shutil
import dataclasses
from distutils.spawn import find_executable
import os
import logging
from . import run_command


logger = logging.getLogger(__name__)


@dataclasses.dataclass
class PythonVersion:
    artifact: typing.Union[str, pathlib.Path]


@dataclasses.dataclass
class UVExecutable:
    name: str


@dataclasses.dataclass
class UvPackageInstallation:
    requirements: typing.List[pathlib.Path]
    extra_pip_args: typing.List[str] = dataclasses.field(default_factory=lambda: [])
    extra_uv_args: typing.List[str] = dataclasses.field(default_factory=lambda: [])


def list_factory():
    return []


protected_paths = set([pathlib.Path("/"), pathlib.Path("/proc"), pathlib.Path("/sys")])


class UVVirtualEnv(Virtualenv):
    def __init__(self, path: typing.Union[str, pathlib.Path], cache_dir: typing.Union[str, pathlib.Path, None] = None):

        self._cache_dir = None
        if path is None or path == "":
            raise RuntimeError("Path is empty")

        if isinstance(path, str):
            path = pathlib.Path(path)

        self.path: pathlib.Path = path

        if self.path in protected_paths:
            raise RuntimeError(f"Cannot install into {self.path}")

        self._uv_executable = find_executable("uv")
        if self._uv_executable is None:
            raise RuntimeError("UV must be installed")

        self._venv_python: typing.Union[pathlib.Path, None] = None

        if cache_dir is not None and cache_dir != "":
            if isinstance(cache_dir, str):
                cache_dir = pathlib.Path(cache_dir)
            self._cache_dir = cache_dir

            if self._cache_dir in protected_paths:
                raise RuntimeError(f"Cannot cache into {self._cache_dir}")

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, UVVirtualEnv):
            return self.path == other.path and self._cache_dir == other._cache_dir
        return False

    @property
    def venv_python(self) -> pathlib.Path:
        if not self._venv_python:
            self._venv_python = pathlib.Path(self._venv_bin("python"))
        return self.venv_python

    def _sanitize_commands(self, cmd: typing.List[str]) -> typing.List[str]:
        return [arg.strip() for arg in cmd if arg != "" and arg != None]

    def initialize(
        self,
        use_system_packages: bool = False,
        extra_pip_args: typing.List[str] = list_factory(),
        extra_uv_args: typing.List[str] = list_factory(),
        clean=True,
    ):
        """Initialize a new uv virtualenv using the specified python version and extra arguments."""

        """
        This differs vrom the VirtualEnv class mainly in that the VirtualEnv class has to determine,
        what python executable is being used and then whether/what pip is to be used inside that
        particular python executable.

        UV has only one binary. It does not require python to be installed an there is no separate
        notion of pip. In other words, if UV is installed then you have everything you need to 
        create a venv
        
        """

        if clean:
            try:
                shutil.rmtree(self.path)
            except OSError:
                # Todo tighten up the  handling
                pass

        # Todo run the actual command
        # Evaluate whether we need preinstall
        # The command needs to look like: uv venv /tmp/ve1 --python 3.10.12

        cache_dir_arg = None
        if self._cache_dir is not None:
            cache_dir_arg = f"--cache-dir={self._cache_dir}"

        command = [self._uv_executable, "venv", cache_dir_arg, str(self.path)] + extra_pip_args + extra_uv_args
        sanitized_command = self._sanitize_commands(command)
        run_command(
            sanitized_command,
            check=True,
        )

    def install(self, installation: UvPackageInstallation):
        """Purge the cache first before installing."""  # (KLAD) testing to debug an issue on build farm

        cache_dir_arg = None
        if self._cache_dir is not None:
            cache_dir_arg = f"--cache-dir={self._cache_dir}"

        command = (
            [self._uv_executable, "pip", "install", cache_dir_arg, "--verbose"]
            + installation.extra_pip_args
            + installation.extra_uv_args
        )

        # https://github.com/astral-sh/uv?tab=readme-ov-file#python-discovery
        #
        install_env = os.environ.copy()
        install_env["VIRTUAL_ENV"] = self.path
        for requirements in installation.requirements:

            sanitized_command = self._sanitize_commands(command + ["-r", str(requirements)])
            run_command(sanitized_command, check=True, env=install_env)

    def lock(self, package_name, input_requirements, no_overwrite, extra_pip_args):
        """Create a frozen requirement set from a set of input specifications."""
        output_requirements = self._get_output_requirements(package_name, input_requirements, no_overwrite)
        pip_compile = self._venv_bin("pip-compile")
        command = [pip_compile, "--no-header", "--annotation-style", "line", input_requirements]
        if extra_pip_args:
            command += ["--pip-args", " ".join(extra_pip_args)]

        command += ["-o", output_requirements]

        run_command(command, check=True)

        logger.info("Wrote new lock file to {}".format(output_requirements))
