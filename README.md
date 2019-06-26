# catkin_virtualenv

[![License: GPL v2](https://img.shields.io/badge/License-GPL%20v2-blue.svg)](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html)

[![Build Status](https://travis-ci.org/locusrobotics/catkin_virtualenv.svg?branch=devel)](https://travis-ci.org/locusrobotics/catkin_virtualenv)

This package provides a mechanism to:

- export python library requirements in `requirements.txt` format via `package.xml`.
- bundle a virtualenv within a catkin package, inheriting requirements from any dependencies.
- wrap python scripts and tests in a catkin package with a virtualenv loader.

At build time, CMake macros provided by this package will create a virtualenv inside the devel space, and create
wrapper scripts for any Python scripts in the package. Both will be included in any associated bloom artifacts.

This library is GPL licensed due to the inclusion of dh_virtualenv.

For general help, please check the [FAQ](http://answers.ros.org/questions/tags:catkin_virtualenv). Report bugs on the [issue tracker](https://github.com/locusrobotics/catkin_virtualenv/issues).

## Exporting python requirements

The package containing python modules with external library dependencies should define a `requirements.txt`:

```python
GitPython>=2.1.5
psutil>=5.2.2
wrapt>=1.10.10
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

This operation does not do any dependency resolution - similar to how `pip` operates, the topmost dependency declaration
'wins' (https://github.com/pypa/pip/issues/988).

Add an build dependency on catkin_virtualenv to `package.xml`, as well as on any library packages you may want. Traditionally

```xml
<build_depend>catkin_virtualenv</build_depend>

<!-- In a catkin/python world, this would normally be an exec_depend. However, if `some_python_library` exports 
requirements.txt, it needs to be pulled in at build time as well -->
<depend>some_python_library</depend>
```

In CMakeLists.txt:

```cmake
# Make sure to find-package `catkin_virtualenv`
find_package(catkin REQUIRED ... catkin_virtualenv ...)

# Must be called before catkin_generate_virtualenv
catkin_package()

# Generate the virtualenv:
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
  # Select an alternative version of the python interpreter - it must be installed on the system. Minor version is optional.
  PYTHON_VERSION 3.7  # Default 2

  # Choose not to use underlying system packages. This excludes any python packages installed by apt or system-pip from the environment.
  USE_SYSTEM_PACKAGES FALSE  # Default TRUE

  # Disable including pip requirements from catkin dependencies of this package.
  ISOLATE_REQUIREMENTS TRUE  # Default FALSE

  # Provide extra arguments to the underlying pip invocation
  EXTRA_PIP_ARGS
    --no-binary=:all:
    -vvv
)
