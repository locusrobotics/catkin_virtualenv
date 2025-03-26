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

from .venv import Virtualenv, _COMMENT_REGEX, _BYTECODE_REGEX
import pathlib
import typing
import sys
import re
import shutil
import dataclasses
from distutils.spawn import find_executable
import os
import logging
from . import run_command


logger = logging.getLogger(__name__)


@dataclasses.dataclass
class PythonVersion:
    version: str = "python3"

    def __post_init__(self):

        match = None
        if self.version.startswith("python"):
            ver = self.version.removeprefix("python")
            if ver == "3":
                match = True
            else:
                match = re.search("3\.[0-9]{1,3}", ver)

        else:
            match = re.search("[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", self.version)
        if match is None:
            raise ValueError("Not a python version or not a UV understood format")


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


def check_package_exists(venv_path: pathlib.Path, package_name: str, cache_dir: pathlib.Path = None) -> bool:
    install_env = os.environ.copy()
    install_env["VIRTUAL_ENV"] = str(venv_path).strip()
    # "--cache-dir", str(cache_dir)
    command = ["uv", "pip", "freeze"]
    completed = run_command(command, check=True, capture_output=True, env=install_env)
    return package_name in completed.stdout.decode()


def check_package_importable():
    pass


def check_package_in_cache(cache_path: pathlib.Path, package_name: str) -> bool:
    c1 = False
    c2 = False
    c3 = False

    for filename in cache_path.glob("**/*"):
        if filename.name == "CACHEDIR.TAG":
            c1 = True
        if filename.name == f"{package_name}.rkyv":
            c2 = True
        if filename.is_dir() and filename.name == package_name:
            c3 = True
    return c1 and c2 and c3


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

    def _build_compile_command(self, requirements: typing.Union[str, pathlib.Path]):

        if isinstance(requirements, pathlib.Path):
            requirements = str(requirements)

        return [
            self._uv_executable,
            "pip",
            "compile",
            "--no-header",
            "--annotation-style",
            "line",
            requirements,
        ]

    def _set_venv_envar(self) -> dict[str, str]:
        install_env = os.environ.copy()
        install_env["VIRTUAL_ENV"] = self.path
        print(self.path)
        return install_env

    # TODO remove pip args
    def initialize(
        self,
        python: PythonVersion = PythonVersion("python3"),
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

        command = (
            [self._uv_executable, "venv", cache_dir_arg, str(self.path), "--python", python.version]
            + extra_pip_args
            + extra_uv_args
        )
        sanitized_command = self._sanitize_commands(command)
        run_command(
            sanitized_command,
            check=True,
        )

    def install(self, installation: UvPackageInstallation):

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
        install_env = self._set_venv_envar()
        for requirements in installation.requirements:

            sanitized_command = self._sanitize_commands(command + ["-r", str(requirements)])
            run_command(sanitized_command, check=True, env=install_env)

    def check(self, requirements: pathlib.Path, extra_uv_args: typing.List = None) -> typing.List[str]:
        """Check if a set of requirements is completely locked."""
        with open(requirements, "r") as f:
            existing_requirements = f.read()

        # Re-lock the requirements
        command = self._build_compile_command(requirements)
        # command += ["-o", "-"]

        # TODO Check what UV supports
        if False and extra_uv_args:
            command += ["--pip-args", " ".join(extra_uv_args)]

        install_env = self._set_venv_envar()
        print(f"Running Command: {' '.join(command)}")
        completed_process = run_command(command, check=False, capture_output=True, env=install_env)
        if completed_process.returncode != 0:
            raise RuntimeError(completed_process.stderr)
        generated_requirements = completed_process.stdout.decode()
        diff = self._diff_requirements(existing_requirements, generated_requirements)
        return diff

    def lock(
        self,
        package_name,
        input_requirements: pathlib.Path,
        no_overwrite: bool,
        extra_pip_args: typing.List[str] = list_factory(),
        test_output_requirements: pathlib.Path = None,  # This is just here because of collect_requirements return value
    ):
        """
        Create a frozen requirement set from a set of input specifications


        Translates to CLI : uv pip compile requirements.in -o requirements.txt

        """
        output_requirements = self._get_output_requirements(package_name, input_requirements, no_overwrite)

        command = self._build_compile_command(input_requirements)
        if extra_pip_args:
            command += ["--pip-args", " ".join(extra_pip_args)]

        # TODO get rid of this once I understand the types of collect_requirements
        output_requirements_path = output_requirements
        if test_output_requirements is not None:
            output_requirements_path = str(test_output_requirements)
        command += ["-o", output_requirements_path]

        run_command(command, check=True)

        logger.info("Wrote new lock file to {}".format(output_requirements_path))
