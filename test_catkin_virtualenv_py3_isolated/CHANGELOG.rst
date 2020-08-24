^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changelog for package test_catkin_virtualenv_py3_isolated
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

0.6.1 (2020-08-24)
------------------
* Correct dependencies and autoformat (`#72 <https://github.com/locusrobotics/catkin_virtualenv/issues/72>`_)
  * Remove python-virtualenv dep
  * Add python2-dev
  * Lint
* Contributors: Paul Bovbel

0.6.0 (2020-07-14)
------------------
* RST-3172 Refactor catkin_virtualenv to allow locking dependencies (`#55 <https://github.com/locusrobotics/catkin_virtualenv/issues/55>`_)
  * Remove unused options
  * Fix regex for comments
  * Migrate scripts
  * Remove old code
  * Move common requirements to an export file
  * Minor cleanup
  * Remove requirement-parsing unit tests
  * Fix logging config
  * Fix test builds
  * Generate lock files
  * Fix tests
  * Move dh-virtualenv functions into separate file
  * Fix roslint
  * Update docs
  * Update requirements
  * CMake comments
  * Fix pip-args
  * README fixup
  * Correct ARG_LOCK_FILE handling
  * Remove headers
  * Use set comprehension
  * Add migration doc
  * Respin
* Contributors: Paul Bovbel

0.5.0 (2019-06-21)
------------------

0.4.1 (2019-06-11)
------------------

0.4.0 (2019-03-18)
------------------
* Fix python3 isolated builds (`#37 <https://github.com/locusrobotics/catkin_virtualenv/issues/37>`_)
  - Pull in an upstream fix to deal with new shebang styles
  - add a new test for isolated py3 virtualenvs
  - switch to using an internal pip module
* Contributors: Paul Bovbel
