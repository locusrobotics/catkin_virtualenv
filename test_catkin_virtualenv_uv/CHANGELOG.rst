^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changelog for package test_catkin_virtualenv
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

0.8.0 (2022-02-23)
------------------

0.9.0 (2023-02-22)
------------------
* 0.8.0
* Update changelogs
* Contributors: Gary Servin

0.10.0 (2023-09-25)
-------------------
* Drop python2 and add Jammy support (#101)
  * Updating pip and pip-tools
  * Trying older version of pip and pip-tools
  * Using slightly newer version of pip and piptools
  * Ensuring we are using python3
  * fix typo
  * Updating catkin-pkg for Jammy support
  * Remove test_virtualenv_python2
  * Update requirements to fix build error
  * Remove python3 direct reference from venv
  * Update pip and pip-tools for 3.7+ compatibility
  * Don't enumerate python versions
  * Add compatibility notes
  * Remove melodic test and python2 references
  * Fix build error more
  * Get rid of requests as a package for testing
  * get_pip isn't versioned 3.6 onwards
  * Fixup double pip-tools
  * Revert "Get rid of requests as a package for testing"
  This reverts commit 55e5b5889d1080303c52fb4e6671d5061498ac57.
  * Try fix action
  * Disable isolated tests
  * Revert changes to match the dependencies
  ---------
  Co-authored-by: Kalpesh Lad <klad@locusrobotics.com>
  Co-authored-by: Gary Servin <gservin@locusrobotics.com>
* 0.9.0
* Update changelogs
* 0.8.0
* Update changelogs
* Revert "Update changelogs"
  This reverts commit 33618e7dec29a058931e5e7190456b4418140c78.
* Update changelogs
* Contributors: Gary Servin, Paul Bovbel

0.11.0 (2024-02-02)
-------------------
* 0.10.0
* Update changelogs
* Drop python2 and add Jammy support (#101)
  * Updating pip and pip-tools
  * Trying older version of pip and pip-tools
  * Using slightly newer version of pip and piptools
  * Ensuring we are using python3
  * fix typo
  * Updating catkin-pkg for Jammy support
  * Remove test_virtualenv_python2
  * Update requirements to fix build error
  * Remove python3 direct reference from venv
  * Update pip and pip-tools for 3.7+ compatibility
  * Don't enumerate python versions
  * Add compatibility notes
  * Remove melodic test and python2 references
  * Fix build error more
  * Get rid of requests as a package for testing
  * get_pip isn't versioned 3.6 onwards
  * Fixup double pip-tools
  * Revert "Get rid of requests as a package for testing"
  This reverts commit 55e5b5889d1080303c52fb4e6671d5061498ac57.
  * Try fix action
  * Disable isolated tests
  * Revert changes to match the dependencies
  ---------
  Co-authored-by: Kalpesh Lad <klad@locusrobotics.com>
  Co-authored-by: Gary Servin <gservin@locusrobotics.com>
* 0.9.0
* Update changelogs
* 0.8.0
* Update changelogs
* Revert "Update changelogs"
  This reverts commit 33618e7dec29a058931e5e7190456b4418140c78.
* Update changelogs
* Contributors: Gary Servin, Paul Bovbel

0.7.0 (2020-10-02)
------------------

0.6.1 (2020-08-24)
------------------
* Correct dependencies and autoformat (`#72 <https://github.com/locusrobotics/catkin_virtualenv/issues/72>`_)
  * Remove python-virtualenv dep
  * Add python2-dev
  * Lint
* Contributors: Paul Bovbel

0.6.0 (2020-07-14)
------------------
* Don't require catkin_package to be called before catkin_generate_virtualenv (`#67 <https://github.com/locusrobotics/catkin_virtualenv/issues/67>`_)
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

0.1.6 (2018-01-10)
------------------

0.1.5 (2018-01-10)
------------------
* Drop strict requirements
* Contributors: Paul Bovbel

0.1.4 (2017-12-03)
------------------
* Fix cmake lint errors
* Add XML schema, README badges, fix travis config for debian jessie, and remove legacy scripts
* Merge pull request `#5 <https://github.com/locusrobotics/catkin_virtualenv/issues/5>`_ from gavanderhoorn/manifest_fix
  Remove stray 's' from test package manifests.
* Remove stray 's' from test package manifests.
* Contributors: Paul Bovbel, gavanderhoorn

0.1.3 (2017-11-27)
------------------

0.1.2 (2017-11-23)
------------------
* Drop rosbash dependency and move python scripts into cmake directory
* More tweaks to get nosetests working in python3
* Contributors: Paul Bovbel

0.1.1 (2017-11-22)
------------------

0.1.0 (2017-11-22)
------------------
* Fix trusty support
* Contributors: Paul Bovbel

0.0.1 (2017-11-22)
------------------
* Add license
* Overhaul virtualenv generation and add Python 3 support (`#1 <https://github.com/locusrobotics/catkin_virtualenv/issues/1>`_)
  * Rewrite build_venv in python
  * Use dh_virtualenv to do the heavy lifting; embed new version of dh_virtualenv internally
  * Update CMake to generate virtualenv appropriately for install and devel space
* Initial implementation
* Contributors: Paul Bovbel
