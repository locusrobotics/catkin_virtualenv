from catkin_virtualenv.cli import (
    _parse_init_args,
    _build_sanitized_extra_args,
    _parse_install_args,
    diff_check,
    _parse_check_args,
)
import unittest
import tempfile
import pathlib
import shutil


class TestBuildSanitizedExtraPipArgs(unittest.TestCase):

    def test_parse_none(self):
        args = _parse_init_args(["python3"])
        result = _build_sanitized_extra_args(args, True)
        self.assertEqual(result, [])

        args = _parse_init_args(["python3"])
        result = _build_sanitized_extra_args(args, False)
        self.assertEqual(result, [])


class TestInitArgs(unittest.TestCase):

    def setUp(self) -> None:
        self._venv_path = "/tmp/venv"
        self._python_binary = "python3"
        self._uv_cache = "/tmp/test/uv"
        return super().setUp()

    def test_parses_virtualenv_args(self):

        args = _parse_init_args(
            [
                self._venv_path,
                "--python",
                self._python_binary,
            ]
        )
        self.assertIsNotNone(args)
        self.assertEqual(args.venv, self._venv_path)
        self.assertEqual(args.python, self._python_binary)

    def test_parses_virtualenv_system_packages(self):

        args = _parse_init_args([self._venv_path, "--python", self._python_binary, "--use-system-packages"])
        self.assertTrue(args.use_system_packages)

    def test_no_uv(self):
        args = _parse_init_args([self._python_binary])
        self.assertFalse(args.use_uv)
        self.assertIsNone(args.uv_cache)

    def test_uv(self):

        args = _parse_init_args(
            [self._venv_path, "--python", self._python_binary, "--use-uv", "--uv-cache", self._uv_cache]
        )
        self.assertTrue(args.use_uv)
        self.assertIsNotNone(args.uv_cache)
        self.assertEqual(args.uv_cache, self._uv_cache)

    def test_cannot_set_system_packages_and_uv(self):

        with self.assertRaises(ValueError) as ve:
            args = _parse_init_args(
                [self._python_binary, "--use-system-packages", "--use-uv", "--uv-cache", self._uv_cache]
            )

    def test_cannot_set_pip_args_and_uv(self):

        with self.assertRaises(ValueError) as ve:
            args = _parse_init_args(
                [
                    self._python_binary,
                    "--use-system-packages",
                    "--use-uv",
                    "--uv-cache",
                    self._uv_cache,
                    "--extra-pip-args",
                    "-qq 10",
                ]
            )


class TestInstallArgs(unittest.TestCase):

    def setUp(self) -> None:
        self._venv_path = "/tmp/venv"
        self._uv_cache = "/tmp/test/uv"
        self._requirements = "/tmp/requirements.txt"
        return super().setUp()

    def test_parses_virtualenv_args(self):

        args = _parse_install_args([self._venv_path, "--requirements", self._requirements])
        self.assertIsNotNone(args)
        self.assertEqual(args.venv, self._venv_path)

    def test_no_uv(self):
        args = _parse_install_args([self._venv_path, "--requirements", self._requirements])
        self.assertFalse(args.use_uv)
        self.assertIsNone(args.uv_cache)


class TestCheckArgs(unittest.TestCase):

    def setUp(self) -> None:
        self._venv_path = "/tmp/venv"
        self._requirements = "/tmp/requirements.txt"
        return super().setUp()

    def test_check_args(self):
        _parse_check_args([self._venv_path, "--requirements", self._requirements])


class TestDiffCheck(unittest.TestCase):

    def setUp(self) -> None:
        self._xunit_output = pathlib.Path(tempfile.mkdtemp()) / "xunit_output.xml"
        return super().setUp()

    def tearDown(self) -> None:
        shutil.rmtree(self._xunit_output, ignore_errors=True)
        return super().tearDown()

    def test_diff(self):
        diff_check(self._xunit_output, ["requests==2.2.2"], ["numpy==1.0.1"])

        failure_found = False
        numpy_found = False
        requests_found = False
        lines = []
        with open(self._xunit_output, "r") as f:
            lines = f.readlines()

        for line in lines:
            if 'failures="1"' in line:
                failure_found = True
            if "numpy==1.0.1" in line:
                numpy_found = True
            if "The following changes would fully lock ['requests==2.2.2']" in line:
                requests_found = True

        self.assertTrue(failure_found)
        self.assertTrue(numpy_found)
        self.assertTrue(requests_found)
