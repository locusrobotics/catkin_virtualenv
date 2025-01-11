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
import unittest

from catkin_virtualenv.uvvenv import UVVirtualEnv, UvPackageInstallation, PythonVersion, check_package_in_cache
from catkin_virtualenv import run_command
import pathlib
import mock
import tempfile
import uuid
import shutil


REQUIREMENTS_TXT = pathlib.Path(__file__).resolve().parent / "testdata" / "requirements.txt"
REQUIREMENTS_IN = pathlib.Path(__file__).resolve().parent / "testdata" / "requirements.in"
SECOND_REQUIREMENTS_TXT = pathlib.Path(__file__).resolve().parent / "testdata" / "second-requirements.txt"
OTA_REQUIREMENTS_IN = pathlib.Path(__file__).resolve().parent / "testdata" / "ota-requirements.in"
OTA_REQUIREMENTS_GOOD_TXT = pathlib.Path(__file__).resolve().parent / "testdata" / "ota-good-requirements.txt"
OTA_REQUIREMENTS_BAD_TXT = pathlib.Path(__file__).resolve().parent / "testdata" / "ota-bad-requirements.txt"

TMP_CATKIN_LOCUSVIRTUALENV = "catkin_locusvirtualenv"
TMP_CATKIN_LOCUSVIRTUALENV_CACHE = "catkin_locusvirtualenv_cache_dir"

EXISTING_REQUIREMENTS = "certifi==2022.12.7        # via requests\ncffi==1.15.1\ncharset-normalizer==3.1.0  # via requests\nidna==3.4                 # via requests\npackaging==23.1\npycparser==2.21           # via cffi\nrequests==2.29.0\nurllib3==1.26.15          # via requests\n"
GENERATED_REQUIREMENTS = "certifi==2022.12.7        # via requests\ncffi==1.15.1\ncharset-normalizer==3.1.0  # via requests\nidna==3.4                 # via requests\npackaging==23.1\npycparser==2.21           # via cffi\nrequests==2.29.0\nurllib3==1.26.15          # via requests\n"
BAD_GENERATED_REQUIREMENTS = "ncffi==1.15.1\ncharset-normalizer==3.1.0  # via requests\nidna==3.4                 # via requests\npackaging==23.1\npycparser==2.21           # via cffi\nrequests==2.29.0\nurllib3==1.26.15          # via requests\n"


class UVVirtualEnvTestCase(unittest.TestCase):
    """
    These test are not true unit tests.
    Some tests require network access in order to download packages.
    If network or package repositories are down, then tests may fail.

    The tests also require disk access.
    All tests use temporary files or directories for i/o.

    """

    def setUp(self) -> None:
        self._venv_dir = pathlib.Path(tempfile.mkdtemp(suffix=TMP_CATKIN_LOCUSVIRTUALENV))
        self._cache_path = pathlib.Path(tempfile.mkdtemp(suffix=TMP_CATKIN_LOCUSVIRTUALENV_CACHE))

        self._first_venv_name = str(uuid.uuid4())
        self._full_first_venv_path = self._venv_dir / self._first_venv_name
        self._first_uv_venv = UVVirtualEnv(self._full_first_venv_path, self._cache_path)

        self._second_venv_name = str(uuid.uuid4())
        self._full_second_venv_path = self._venv_dir / self._second_venv_name
        self._second_uv_venv = UVVirtualEnv(self._full_second_venv_path, self._cache_path)

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

        parent = pathlib.Path(self._venv_dir).parent
        shutil.rmtree(self._venv_dir)

        # The above will normally clean up directories
        # Sometimes, mainly when debugging directories are leftover
        # The below will clean up matching dir names
        for file in parent.iterdir():
            base_name = str(file.name)
            c1 = file.is_dir()
            c2 = TMP_CATKIN_LOCUSVIRTUALENV_CACHE in base_name
            c3 = TMP_CATKIN_LOCUSVIRTUALENV in base_name
            if c1 and (c2 or c3):
                shutil.rmtree(file)

        return super().tearDown()


class TestUVVirtualenv(UVVirtualEnvTestCase):

    def build_package_path(self, venv: UVVirtualEnv, package_name: str) -> pathlib.Path:

        # TODO This is britle with respect to python version.
        return venv.path / "lib/python3.10/site-packages" / package_name

    def check_package_in_cache(self, package_name: str) -> bool:
        """
        Test that a given package is in the UV Cache
        This will search the cache for the package name

        """

        self.assertTrue(check_package_in_cache(self._cache_path, package_name))

    def test_sanity(self):
        """
        Test that we can create a UV Venv object
        """
        UVVirtualEnv(self._venv_dir)

    def test_no_empty_paths(self):
        """
        Test that we must pass a valid path to create a UV Venv
        """
        with self.assertRaises(RuntimeError):
            UVVirtualEnv("")

    def test_no_null_paths(self):
        """
        Test that we must pass a valid path to create a UV Venv
        """
        with self.assertRaises(RuntimeError):
            UVVirtualEnv(None)

    def test_no_protected_paths(self):
        """
        Test that we must pass a valid path to create a UV Venv ( no special locations)
        """
        with self.assertRaises(RuntimeError):
            UVVirtualEnv("/proc")

    def test_equality_for_same_path(self):
        """
        Test that two Venvs are considered equal when based on the same path
        """
        self.assertEqual(UVVirtualEnv("/tmp/foo"), UVVirtualEnv("/tmp/foo"))

    def test_inequality_for_same_path_but_different_cache(self):
        """
        Test that two Venvs are not considered equal when based on the same path but different cache
        """
        self.assertNotEqual(UVVirtualEnv("/tmp/foo", "/tmp/bar"), UVVirtualEnv("/tmp/foo", "/tmp/baz"))

    def test_command_sanitization(self):
        """
        Test that command are sanitized.
        Removes Nones and empty string
        """

        venv = UVVirtualEnv("/tmp/foo")
        expected_result = ["foo", "bar", "baz"]
        actual_result = venv._sanitize_commands(["foo", "bar", "", None, "", "baz"])
        self.assertEqual(expected_result, actual_result)

    def test_init(self):
        """
        Test that we can initialize a UV Venv given a valid path
        This creates a UV Venv
        """
        self._first_uv_venv.initialize()
        self.assertTrue(self._full_first_venv_path.exists)
        python_executable_path = self._full_first_venv_path / "bin" / "python"
        self.assertTrue(python_executable_path.exists())
        self.assertTrue(python_executable_path.is_file())
        self.assertTrue(python_executable_path.is_symlink())

    def test_install(self):
        """
        Test that we can install packages into our venv.
        Checks the path of the packages inside the Venv (not cache)
        """
        self._first_uv_venv.initialize()
        self._first_uv_venv.install(self._default_installation)

        self.assertTrue(self.build_package_path(self._first_uv_venv, "requests").exists())
        self.assertFalse(self.build_package_path(self._first_uv_venv, "flask").exists())

    def test_cache_is_populated(self):
        """
        Test that after we install that the package is inside the cache.
        Checks the path of the packages inside the Cache (not venv)
        """
        self._first_uv_venv.initialize()
        self._first_uv_venv.install(self._default_installation)
        self.check_package_in_cache("requests")

    def test_dual_install(self):
        """
        Test that we can create two different venvs
        Checks the packages installed into the second do not affect the venv of the firsts (and vice versa)
        """
        self._first_uv_venv.initialize()
        self._second_uv_venv.initialize()

        self.assertNotEqual(self._first_uv_venv, self._second_uv_venv)

        self._first_uv_venv.install(self._default_installation)
        self._second_uv_venv.install(self._second_installation)

        self.assertTrue(self.build_package_path(self._first_uv_venv, "requests").exists())
        self.assertFalse(self.build_package_path(self._first_uv_venv, "flask").exists())

        self.assertTrue(self.build_package_path(self._second_uv_venv, "flask").exists())
        self.assertFalse(self.build_package_path(self._second_uv_venv, "requests").exists())

    def test_can_check(self):
        """
        Test that we can lock the Venv
        The mocked call to process_package will return a value that is not in our OTA_REQUIREMENTS_GOOD_TXT
        """
        self._first_uv_venv.initialize()
        self._first_uv_venv.install(UvPackageInstallation(requirements=[OTA_REQUIREMENTS_GOOD_TXT]))
        actual_good_diff = None
        actual_bad_diff = None
        with mock.patch("catkin_virtualenv.collect_requirements.process_package") as process_package_mock:
            process_package_mock.return_value = (["pre-commit"], [])

            actual_good_diff = self._first_uv_venv.check(OTA_REQUIREMENTS_GOOD_TXT)
            actual_bad_diff = self._first_uv_venv.check(OTA_REQUIREMENTS_BAD_TXT)

        self.assertIsNotNone(actual_good_diff)
        self.assertEqual(len(actual_good_diff), 0)
        self.assertGreater(len(actual_bad_diff), 0)

    def test_diff_generation(self):
        """
        Test that our diff resolution works.
        The calls to diff_requirements use pre-canned responses.
        """
        venv = UVVirtualEnv("/tmp/does/not/matter")
        diff = venv._diff_requirements(EXISTING_REQUIREMENTS, GENERATED_REQUIREMENTS)
        self.assertEqual(len(diff), 0)

        bad_diff = venv._diff_requirements(EXISTING_REQUIREMENTS, BAD_GENERATED_REQUIREMENTS)
        self.assertEqual(len(bad_diff), 11)

    def test_python_version(self):
        """
        Test that we don't accept anything but python3 versions.
        """
        PythonVersion("python3")
        PythonVersion("python3.10")
        PythonVersion("3.10.12")
        with self.assertRaises(ValueError):
            PythonVersion("python2")
