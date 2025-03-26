import argparse
import typing

from catkin_virtualenv.venv import Virtualenv
import xml.etree.ElementTree as ET
import inspect
import pathlib

EMPTY_TOKEN = '""'


def diff_check(xunit_output: typing.Union[pathlib.Path, str], requirements: typing.Union[str, pathlib.Path], diff: str):

    if not isinstance(xunit_output, pathlib.Path):
        xunit_output = pathlib.Path(xunit_output)

    if not isinstance(requirements, pathlib.Path):
        requirements = pathlib.Path(requirements)

    if xunit_output.exists() and not xunit_output.is_file():
        raise RuntimeError(f"Xunit Output:{xunit_output} must be a regular file")

    if requirements is None or not isinstance(requirements, pathlib.Path):
        raise RuntimeError("Requirements must not be not none and must be a list")

    if diff is None or not isinstance(diff, list):
        raise RuntimeError("Diff must not be not none and must be a list")

    testsuite = ET.Element("testsuite", name="venv_check", tests="1", failures="1" if diff else "0", errors="0")
    testcase = ET.SubElement(testsuite, "testcase", name="check_locked", classname="catkin_virtualenv.Venv")
    if diff:
        failure = ET.SubElement(testcase, "failure", message="{} is not fully locked".format(requirements))
        message = inspect.cleandoc(
            """
            Consider defining INPUT_REQUIREMENTS to have catkin_virtualenv generate a lock file for this package.
            See https://github.com/locusrobotics/catkin_virtualenv/blob/master/README.md#locking-dependencies.
            The following changes would fully lock {requirements}:
            """.format(
                requirements=requirements
            )
        )
        message += "\n" + "\n".join(diff)
        failure.text = message

    else:
        ET.SubElement(testcase, "success", message="{} is fully locked".format(requirements))

    tree = ET.ElementTree(testsuite)
    tree.write(str(xunit_output), encoding="utf-8", xml_declaration=True)


def _build_sanitized_extra_args(args: argparse.Namespace, use_uv: bool) -> typing.List[str]:

    if use_uv:
        if args.extra_uv_args is None or args.extra_uv_args == EMPTY_TOKEN:
            return []

        extra_uv_args = args.extra_uv_args[1:-1]

        return [arg for arg in extra_uv_args.split(" ") if arg != ""]

    else:

        if args.extra_pip_args is None or args.extra_pip_args == EMPTY_TOKEN:
            return []

        extra_pip_args = args.extra_pip_args[1:-1]

        return [arg for arg in extra_pip_args.split(" ") if arg != ""]


def _parse_init_args(argv: typing.Union[typing.List[str], None]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=Virtualenv.initialize.__doc__)
    parser.add_argument("venv", help="Path where to initialize the virtualenv")
    parser.add_argument("--python", default="python3", help="Build the virtualenv with which python version.")
    parser.add_argument("--use-system-packages", action="store_true", help="Use system site packages.")
    parser.add_argument("--use-uv", action="store_true", help="Use uv for deduplication.")
    parser.add_argument("--uv-cache", default=None, help="Cache dir for UV.")
    parser.add_argument("--extra-pip-args", default=EMPTY_TOKEN, type=str, help="Extra pip args for install.")
    parser.add_argument("--extra-uv-args", default=EMPTY_TOKEN, type=str, help="Extra uv args for install.")

    namespace = parser.parse_args(argv)

    if namespace.use_system_packages and namespace.use_uv:
        raise ValueError("Cannot set both '--use-system-packages' and '--use-uv' ")

    if namespace.extra_pip_args != EMPTY_TOKEN and namespace.use_uv:
        print(f"ExtraPipArgs:{namespace.extra_pip_args}")
        raise ValueError(f"Cannot set both '--extra-pip-args' and '--use-uv' \n {namespace.extra_pip_args} ")

    if namespace.extra_pip_args != EMPTY_TOKEN and namespace.extra_uv_args != EMPTY_TOKEN:
        raise ValueError("Cannot set both '--extra-pip-args' and '--extra-uv-args' ")

    return namespace


def _parse_install_args(argv: typing.Union[typing.List[str], None]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=Virtualenv.install.__doc__)
    parser.add_argument("venv", help="Path of virtualenv to manage.")
    parser.add_argument("--use-uv", action="store_true", help="Use uv for deduplication.")
    parser.add_argument("--uv-cache", default=None, help="Cache dir for UV.")
    parser.add_argument("--requirements", required=True, nargs="+", help="Requirements to sync to virtualenv.")
    parser.add_argument("--extra-pip-args", default='""', type=str, help="Extra pip args for install.")
    parser.add_argument("--extra-uv-args", default='""', type=str, help="Extra uv args for install.")

    return parser.parse_args(argv)


def _parse_check_args(argv: typing.Union[typing.List[str], None]) -> argparse.Namespace:

    parser = argparse.ArgumentParser(description=Virtualenv.install.__doc__)
    parser.add_argument("venv", help="Path of virtualenv to manage.")
    parser.add_argument("--use-uv", action="store_true", help="Use uv for deduplication.")
    parser.add_argument("--requirements", required=True, help="Requirements to check.")
    parser.add_argument("--extra-pip-args", default='""', type=str, help="Extra pip args for install.")
    parser.add_argument("--extra-uv-args", default='""', type=str, help="Extra uv args for install.")
    parser.add_argument("--xunit-output", help="Destination where to write xunit output.")

    return parser.parse_args()
