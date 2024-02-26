#!/usr/bin/env python
# Software License Agreement (GPL)
#
# \file      test_virtualenv_script
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
import importlib
import unittest

from catkin_virtualenv.uvvenv import UVVirtualEnv, UvPackageInstallation
from packaging import version
import pathlib
import tempfile
import uuid
import shutil


REQUIREMENTS_TXT = pathlib.Path(__file__).resolve().parent / "testdata" / "requirements.txt"
REQUIREMENTS_IN = pathlib.Path(__file__).resolve().parent / "testdata" / "requirements.in"
SECOND_REQUIREMENTS_TXT = pathlib.Path(__file__).resolve().parent / "testdata" / "second-requirements.txt"


class TestUVVirtualenv(unittest.TestCase):

    def setUp(self) -> None:
        self._venv_dir = pathlib.Path(tempfile.mkdtemp(suffix="catkin_locusvirtualenv"))

        self._first_venv_name = str(uuid.uuid4())
        self._full_first_venv_path = self._venv_dir / self._first_venv_name
        self._first_uv_venv = UVVirtualEnv(self._full_first_venv_path)

        self._second_venv_name = str(uuid.uuid4())
        self._full_second_venv_path = self._venv_dir / self._second_venv_name
        self._second_uv_venv = UVVirtualEnv(self._full_second_venv_path)

        if not REQUIREMENTS_TXT.exists():
            raise RuntimeError("Requirements.txt not in expected location")

        if not REQUIREMENTS_IN.exists():
            raise RuntimeError("Requirements.in not in expected location")

        if not SECOND_REQUIREMENTS_TXT.exists():
            raise RuntimeError("Second-Requirements.txt not in expected location")

        self._default_installation = UvPackageInstallation(requirements=[REQUIREMENTS_TXT])
        self._second_installation = UvPackageInstallation(requirements=[SECOND_REQUIREMENTS_TXT])

        return super().setUp()

    def tearDown(self) -> None:

        shutil.rmtree(self._venv_dir)
        return super().tearDown()

    def build_package_path(self, venv: UVVirtualEnv, package_name: str) -> pathlib.Path:

        # TODO This is britle with respect to python version.
        return venv.path / "lib/python3.10/site-packages" / package_name

    def test_sanity(self):
        UVVirtualEnv(self._venv_dir)

    def test_no_empty_paths(self):
        with self.assertRaises(RuntimeError):
            UVVirtualEnv("")

    def test_no_null_paths(self):
        with self.assertRaises(RuntimeError):
            UVVirtualEnv(None)

    def test_no_protected_paths(self):
        with self.assertRaises(RuntimeError):
            UVVirtualEnv("/proc")

    def test_init(self):
        self._first_uv_venv.initialize()
        self.assertTrue(self._full_first_venv_path.exists)
        python_executable_path = self._full_first_venv_path / "bin" / "python"
        self.assertTrue(python_executable_path.exists())
        self.assertTrue(python_executable_path.is_file)

    def test_install(self):
        self._first_uv_venv.initialize()
        self._first_uv_venv.install(self._default_installation)

        self.assertTrue(self.build_package_path(self._first_uv_venv, "requests").exists())
        self.assertFalse(self.build_package_path(self._first_uv_venv, "flask").exists())

    def test_dual_install(self):
        self._first_uv_venv.initialize()
        self._second_uv_venv.initialize()

        self.assertNotEqual(self._first_uv_venv, self._second_uv_venv)

        self._first_uv_venv.install(self._default_installation)
        self._second_uv_venv.install(self._second_installation)

        self.assertTrue(self.build_package_path(self._first_uv_venv, "requests").exists())
        self.assertFalse(self.build_package_path(self._first_uv_venv, "flask").exists())

        self.assertTrue(self.build_package_path(self._second_uv_venv, "flask").exists())
        self.assertFalse(self.build_package_path(self._second_uv_venv, "requests").exists())
