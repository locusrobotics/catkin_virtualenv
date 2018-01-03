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

## Exporting python requirements:

The package containing python modules with external library dependencies should define a `requirements.txt`:

```
GitPython>=2.1.5
psutil>=5.2.2
wrapt>=1.10.10
```

Add an export to `package.xml`:

```
<export>
  <pip_requirements>requirements.txt</pip_requirements>
</export>
```

Make sure to install the requirements file in `CMakeLists.txt`:

```
install(FILES requirements.txt
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})
```

## Bundling virtualenv:

It's possible to bundle all of a catkin package's python requirements, as well as those of its catkin dependencies,
into a virtualenv. This process will also override the standard `catkin_install_python` macro to wrap a virtualenv
loader around the specified python scripts.

Add an build dependency to `package.xml`:

```
<build_depend>catkin_virtualenv</build_depend>
```

In CMakeLists.txt:

```
# Make sure to find-package `catkin_virtualenv`
find_package(catkin REQUIRED ... catkin_virtualenv ...)

# Generate the virtualenv, optionally with python 3 as the default interpreter:
catkin_generate_virtualenv()
# catkin_generate_virtualenv(PYTHON3)

# Make sure your python executables are installed using `catkin_install_python`:
catkin_install_python(
  PROGRAMS
    scripts/do_python_things
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION})
```

Departing from convention, if these scripts are executable, `catkin build` will make them non-executable. This is
because `catkin_install_python` will now generate new wrapper scripts into the devel and install space that bootstrap
the virtualenv and `rosrun` gets confused if there's two executable scripts by the same name.

Unit and integration tests will automatically pick up the virtualenv as well. The only change is to add a dependency 
from the test target to the virtualenv target:

```
if(CATKIN_ENABLE_TESTING)

  # nosetests
  catkin_add_nosetests(test
    DEPENDENCIES ${PROJECT_NAME}_generate_virtualenv
  )

  # rostests
  find_package(rostest)
  catkin_install_python(
    PROGRAMS
      test/test_script
    DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION})

  add_rostest(test/run_test_script.test
    DEPENDENCIES ${PROJECT_NAME}_generate_virtualenv
  )
)
```
