^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changelog for package test_catkin_virtualenv_isolated
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

0.8.0 (2022-02-23)
------------------
* Switch default interpreter to python3 (#77)
  * Switch default interpreter to python3
  * Remove python2
  * Add back vitualenv, needed for python2
  * Tailor: Updating Jenkinsfile
  Co-authored-by: Gary Servin <gservin@locusrobotics.com>
  Co-authored-by: locus-services <33065330+locus-services@users.noreply.github.com>
* Contributors: Paul Bovbel

Forthcoming
-----------

0.9.0 (2023-02-22)
------------------
* 0.8.0
* Update changelogs
* Fix catkin_virtualenv for python2 (#92)
  * Add python2 test package
  * Fix dependencies for python2
  * Skip python2 for noetic upstream
* Switch default interpreter to python3 (#77)
  * Switch default interpreter to python3
  * Remove python2
  * Add back vitualenv, needed for python2
  * Tailor: Updating Jenkinsfile
  Co-authored-by: Gary Servin <gservin@locusrobotics.com>
  Co-authored-by: locus-services <33065330+locus-services@users.noreply.github.com>
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
