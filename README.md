# catkin_virtualenv

[![License: GPL v2](https://img.shields.io/badge/License-GPL%20v2-blue.svg)](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html)

This package provides a mechanism to:

- export python `pip` requirements via `package.xml`.
- bundle a virtualenv within a catkin package, inheriting requirements from any dependencies.
- wrap python scripts and tests in a catkin package with a virtualenv loader.
- change which interpreter is used for executing scripts and tests (i.e. python2, python3, pypy, etc.)

At build time, CMake macros provided by this package will create a virtualenv inside the devel space, and create
wrapper scripts for any Python scripts in the package. Both will be included in any associated bloom artifacts.

This library is GPL licensed due to the inclusion of dh_virtualenv.

For general help, please check the [FAQ](http://answers.ros.org/questions/tags:catkin_virtualenv). Report bugs on the [issue tracker](https://github.com/locusrobotics/catkin_virtualenv/issues).

## Exporting python requirements

A package containing python modules with external `pip` dependencies should define a `requirements.txt`:

```python
GitPython==2.1
psutil==5.2.2
```

Add an export to `package.xml`:

```xml
<export>
  <pip_requirements>requirements.txt</pip_requirements>
</export>
```

Make sure to install the requirements file in `CMakeLists.txt`:

```cmake
install(FILES requirements.txt
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})
```

If a catkin package exports dependencies in a `requirements.txt` file, any dependent catkin package that bundles a virtualenv (see below) will inherit those dependencies.



## Bundling virtualenv

It's possible to bundle all of a catkin package's python requirements, as well as those of its catkin dependencies,
into a virtualenv. This process will also override the standard `catkin_install_python` macro to wrap a virtualenv
loader around the specified python scripts.

Add an build dependency on catkin_virtualenv to `package.xml`, as well as on any library packages you may want. Traditionally

```xml
<build_depend>catkin_virtualenv</build_depend>

<!-- In a catkin/python world, this would normally be an exec_depend. However, if `some_python_library` exports
requirements.in, it needs to be pulled in at build time as well -->
<depend>some_python_library</depend>
```

In CMakeLists.txt:

```cmake
# Make sure to find-package `catkin_virtualenv`
find_package(catkin REQUIRED ... catkin_virtualenv ...)

# Generate the virtualenv
catkin_generate_virtualenv()

# Make sure your python executables are installed using `catkin_install_python`:
catkin_install_python(
  PROGRAMS
    scripts/do_python_things
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION})
```

Departing from convention, `scripts/do_python_things` should not be executable, and `catkin build` will warn to that effect.
This package works by hijacking `catkin_install_python` to generate new wrapper scripts into the devel and install space,
which bootstrap the `virtualenv`. In addition, `rosrun` gets confused if there's two executable files with the same name.

Unit and integration tests will automatically pick up the `virtualenv` as well. The only change is to add a dependency
from the test target to the virtualenv target:

```cmake
if(CATKIN_ENABLE_TESTING)

  # nosetests
  catkin_add_nosetests(test
    DEPENDENCIES ${PROJECT_NAME}_generate_virtualenv
  )

  # rostests
  catkin_install_python(
    PROGRAMS
      test/test_script
    DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION})

  add_rostest(test/run_test_script.test
    DEPENDENCIES ${PROJECT_NAME}_generate_virtualenv
  )
)
```

### Additional CMake Options

The following options are supported by `catkin_generate_virtualenv()`:

```cmake
catkin_generate_virtualenv(
  # Specify the input requirements for this package that catkin_virtualenv will automatically lock.
  INPUT_REQUIREMENTS requirements.in

  # Select an alternative python interpreter - it must be installed on the system.
  PYTHON_INTERPRETER python3.7  # Default python3

  # Choose not to use underlying system packages. This excludes any python packages installed by apt or system-pip from the environment.
  USE_SYSTEM_PACKAGES FALSE  # Default TRUE

  # Disable including pip requirements from catkin dependencies of this package.
  ISOLATE_REQUIREMENTS TRUE  # Default FALSE

  # Disable creating a unit test to verify that package requirements are locked.
  CHECK_VENV FALSE  # Default TRUE
  
  # Disable renaming the process names to hide the interpreter name, this has can create issues when executing the process as root.
  RENAME_PROCESS FALSE # Default TRUE

  # Provide extra arguments to the underlying pip invocation
  EXTRA_PIP_ARGS
    --no-binary=:all:
    -vvv
)
```

### Locking dependencies

This project allows you to lock dependencies by leveraging `pip-compile`. This is optional, but will prevent your
python projects from spontaneously combusting in the future!

Instead of managing a `requirements.txt` file, you will manage a `requirements.in` file, and catkin_virtualenv will generate the `requirements.txt` file for you upon build.

Create a `requirements.in` file and populate it manually with your package's requirements. For example:

```python
GitPython>=2
psutil
```

The file specified in CMake options as `INPUT_REQUIREMENTS` will be used to generate a locked `requirements.txt`
at build time. You should check both `requirements.in` and `requirements.txt` in with your sources!

To regenerate the `requirements.txt` file, either delete it and rebuild the project, or run this command from your project directory:

`catkin build --this --no-deps --catkin-make-args <PROJECT_NAME>_venv_lock` where `<PROJECT_NAME>` is the name for the project as specified in the package's CMakeLists.txt.

Alternatively, you can specify the package name `catkin build <PACKAGE_NAME> --no-deps --catkin-make-args <PROJECT_NAME>_venv_lock`

To migrate a package from catkin_virtualenv <=0.5 to use lock files:

- Rename `requirements.txt` to `requirements.in`
- Relax the version requirements in `requirements.in` as much as sensibly possible. eg. requests>=2  vs. requests=2.23.0
- Add `INPUT_REQUIREMENTS requirements.in` to catkin_generate_virtualenv() in CMakeLists.txt
- Build and test that the package given the installed dependency versions might have changed slightly
- Commit the new `requirements.in`, your updated `CMakeLists.txt` and the new version of `requirements.txt` and push changes

See example: https://github.com/locusrobotics/aiorospy/pull/30/commits/839b17adbe0c672f5e0d9cca702d12e16b117bca
