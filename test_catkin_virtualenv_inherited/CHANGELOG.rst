^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changelog for package test_catkin_virtualenv_inherited
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

0.6.1 (2020-08-24)
------------------
* Correct dependencies and autoformat (`#72 <https://github.com/locusrobotics/catkin_virtualenv/issues/72>`_)
  * Remove python-virtualenv dep
  * Add python2-dev
  * Lint
* Contributors: Paul Bovbel

0.6.0 (2020-07-14)
------------------
* Remove user specific paths (`#63 <https://github.com/locusrobotics/catkin_virtualenv/issues/63>`_)
  * Remove user specific paths
  * Change working directory of venv_lock command
  * Lock catkin_virtualenv base requirements
  Co-authored-by: Paul Bovbel <paul@bovbel.com>
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
* Contributors: David V. Lu!!, Paul Bovbel

0.5.0 (2019-06-21)
------------------

0.4.1 (2019-06-11)
------------------

0.4.0 (2019-03-18)
------------------

0.3.0 (2019-01-16)
------------------
* Python3 re-enable, add PYTHON_VERSION support (`#33 <https://github.com/locusrobotics/catkin_virtualenv/issues/33>`_)
  * replace PYTHON_VERSION_MAJOR with PYTHON_VERSION
  * Simplify nose usage for python3
  * Check for venv module directly rather than munging major version
* Contributors: Paul Bovbel

0.2.2 (2018-12-04)
------------------
* Merge repeated requirements (`#32 <https://github.com/locusrobotics/catkin_virtualenv/issues/32>`_)
* Contributors: Paul Bovbel

0.2.1 (2018-06-04)
------------------

0.2.0 (2018-05-03)
------------------

0.1.6 (2018-01-10 12:05)
------------------------

0.1.5 (2018-01-10 11:15)
------------------------

0.1.4 (2017-12-03)
------------------

0.1.3 (2017-11-27)
------------------

0.1.2 (2017-11-23)
------------------

0.1.1 (2017-11-22 17:42)
------------------------

0.1.0 (2017-11-22 17:30)
------------------------

0.0.1 (2017-11-22 14:14)
------------------------
