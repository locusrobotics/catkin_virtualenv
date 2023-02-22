^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changelog for package catkin_virtualenv
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

0.8.0 (2022-02-23)
------------------
* Switch default interpreter to python3 (#77)
  * Switch default interpreter to python3
  * Remove python2
  * Add back vitualenv, needed for python2
  * Tailor: Updating Jenkinsfile
  Co-authored-by: Gary Servin <gservin@locusrobotics.com>
  Co-authored-by: locus-services <33065330+locus-services@users.noreply.github.com>
* Bump dependencies (#76)
  * Bump dependencies
  * Drop kinetic
* Contributors: Paul Bovbel

0.9.0 (2023-02-22)
------------------
* 0.8.0
* Update changelogs
* Use upstream to configure logging (#94)
* Allow disabling process rename when it creates issues (#93)
* Check ensurepip to install pip via get-pip.py (#90)
  * Check ensurepip to install pip via get-pip.py
  * Add ImportError to pass lint
* Fix catkin_virtualenv for python2 (#92)
  * Add python2 test package
  * Fix dependencies for python2
  * Skip python2 for noetic upstream
* Rename process to program name (#50)
  * Rename process to node name
  * Rethink approach
  * Mirror how native processes are named
  * Bump dependencies
  * Try heredoc bash to python interp
* Run catkin_run_tests_target only when CATKIN_ENABLE_TESTING is enabled (#89)
* use PROJECT_SOURCE_DIR for requirements in venv_lock (#88)
* Make CMake work in non-isolated builds. (#87)
  * Make CMake work in non-isolated builds.
  Specifically when `catkin_virtualenv` was used in multiple packages.
  * Updated docs.
  Removed split between isolated and non-isolated `venv_lock` targets.
* fix rospkg to 1.3.0 (#85)
* Improved _venv_bin to find binaries in local (#81)
  Co-authored-by: Jorge López Fueyo <jorge@scaledrobotics.com>
* Switch default interpreter to python3 (#77)
  * Switch default interpreter to python3
  * Remove python2
  * Add back vitualenv, needed for python2
  * Tailor: Updating Jenkinsfile
  Co-authored-by: Gary Servin <gservin@locusrobotics.com>
  Co-authored-by: locus-services <33065330+locus-services@users.noreply.github.com>
* Bump dependencies (#76)
  * Bump dependencies
  * Drop kinetic
* Contributors: Alec Tiefenthal, Gary Servin, Iori Yanokura, Jorge López Fueyo, Paul Bovbel, Shingo Kitagawa, Yuki Furuta

0.7.0 (2020-10-02)
------------------

0.6.1 (2020-08-24)
------------------
* Correct dependencies and autoformat (`#72 <https://github.com/locusrobotics/catkin_virtualenv/issues/72>`_)
  * Remove python-virtualenv dep
  * Add python2-dev
  * Lint
* We're ok with any 44.x version of setuptools (`#71 <https://github.com/locusrobotics/catkin_virtualenv/issues/71>`_)
  But not anything newer.
  Older versions don't appear to work reliably with `pip==20.1`.
  This helps when running a build of a package depending on catkin_virtualenv on OS which ship with an old version of setuptools (such as Ubuntu Xenial) when `USE_SYSTEM_PACKAGES` is not set to `FALSE`. In that situation, only specifying 'setuptools<45` will be true, as setuptools is installed (in the systems site packages), so pip will not upgrade it. Specifying a minimum version like this will force pip to always install an up-to-date version.
* Contributors: G.A. vd. Hoorn, Paul Bovbel

0.6.0 (2020-07-14)
------------------
* Don't require catkin_package to be called before catkin_generate_virtualenv (`#67 <https://github.com/locusrobotics/catkin_virtualenv/issues/67>`_)
* Revert "Downgrade docutils so that boto works (`#66 <https://github.com/locusrobotics/catkin_virtualenv/issues/66>`_)"
  This reverts commit 998cd6add2e43e12036d0db15a7c4d58fe3411cf.
* Downgrade docutils so that boto works (`#66 <https://github.com/locusrobotics/catkin_virtualenv/issues/66>`_)
  See https://github.com/boto/botocore/issues/1942 and related threads.
* Make regex for Python bytecode more selective (`#65 <https://github.com/locusrobotics/catkin_virtualenv/issues/65>`_)
  Fix regex to match only files ending in ".py[co]" and not files ending
  in "py[co]".
* Remove user specific paths (`#63 <https://github.com/locusrobotics/catkin_virtualenv/issues/63>`_)
  * Remove user specific paths
  * Change working directory of venv_lock command
  * Lock catkin_virtualenv base requirements
  Co-authored-by: Paul Bovbel <paul@bovbel.com>
* RST-3172 Check that requirements file is locked (`#62 <https://github.com/locusrobotics/catkin_virtualenv/issues/62>`_)
* Two helpful hints (`#61 <https://github.com/locusrobotics/catkin_virtualenv/issues/61>`_)
* Fix input requirements warning (`#58 <https://github.com/locusrobotics/catkin_virtualenv/issues/58>`_)
  * Only warn about INPUT_REQUIREMENTS if a package exports requirements to begin with
  * Update catkin_virtualenv/cmake/catkin_generate_virtualenv.cmake
  Co-authored-by: Andrew Blakey <ablakey@gmail.com>
  Co-authored-by: Andrew Blakey <ablakey@gmail.com>
* Preserve symlinks during copy (`#57 <https://github.com/locusrobotics/catkin_virtualenv/issues/57>`_)
* Don't ignore unknown args
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
* Use exec to dive into python (`#51 <https://github.com/locusrobotics/catkin_virtualenv/issues/51>`_)
* First python2 issue of 2020 (`#49 <https://github.com/locusrobotics/catkin_virtualenv/issues/49>`_)
  * Clean up options, virtualenv installs setuptools by default
  * Make sure we install a compatible setuptools version for py2 venv
* catkin-pkg-modules has disappeared off pypi (`#46 <https://github.com/locusrobotics/catkin_virtualenv/issues/46>`_)
  * catkin-pkg-modules has disappeared off pypi, but catkin-pkg is still there
  * Version all requirements
* Contributors: David V. Lu!!, Michael Johnson, Paul Bovbel, abencz

0.5.0 (2019-06-21)
------------------
* Don't inherit requirements from exec_depends (`#45 <https://github.com/locusrobotics/catkin_virtualenv/issues/45>`_)
* Contributors: Paul Bovbel

0.4.1 (2019-06-11)
------------------
* VCS support (`#40 <https://github.com/locusrobotics/catkin_virtualenv/issues/40>`_)
* Contributors: Paul Bovbel

0.4.0 (2019-03-18)
------------------
* Pin pip to known-working version (`#38 <https://github.com/locusrobotics/catkin_virtualenv/issues/38>`_)
* Fix python3 isolated builds (`#37 <https://github.com/locusrobotics/catkin_virtualenv/issues/37>`_)
  - Pull in an upstream fix to deal with new shebang styles
  - add a new test for isolated py3 virtualenvs
  - switch to using an internal pip module
* venv module doesn't support no-site-packages arg
* Pass arguments to internal venv module if specified (`#36 <https://github.com/locusrobotics/catkin_virtualenv/issues/36>`_)
* Add missing dependency
* Contributors: Paul Bovbel

0.3.0 (2019-01-16)
------------------
* Add retry to virtualenv creation (`#34 <https://github.com/locusrobotics/catkin_virtualenv/issues/34>`_)
  * Echo check_call to stderr
  * Fixup bug from `#33 <https://github.com/locusrobotics/catkin_virtualenv/issues/33>`_
  * Add retry to virtualenv generation
  * Add debug line for virtualenv
  * Don't error on cleanup
  * Fixup debug line
  * Remove debug lines
* Python3 re-enable, add PYTHON_VERSION support (`#33 <https://github.com/locusrobotics/catkin_virtualenv/issues/33>`_)
  * replace PYTHON_VERSION_MAJOR with PYTHON_VERSION
  * Simplify nose usage for python3
  * Check for venv module directly rather than munging major version
* Remove trailing whitespace
* Add missing dependencies
* Contributors: Paul Bovbel

0.2.2 (2018-12-04)
------------------
* Merge repeated requirements (`#32 <https://github.com/locusrobotics/catkin_virtualenv/issues/32>`_)
* Enable extra_pip_args `#31 <https://github.com/locusrobotics/catkin_virtualenv/issues/31>`_ from locusrobotics/add-extra-pip-args
* Contributors: Brian Barnes, Paul Bovbel, Shingo Kitagawa

0.2.1 (2018-06-04)
------------------
* Fix case and '.' handling
* Bump pip to 10.0.1
* Contributors: Paul Bovbel

0.2.0 (2018-05-03)
------------------
* Fixup python 3 dependencies
* Merge pull request `#16 <https://github.com/locusrobotics/catkin_virtualenv/issues/16>`_ from locusrobotics/system-site-packages
  Provide more CMake flags to customize behaviour
* Make sure we find python exectuable
* Implement ISOLATE_REQUIREMENTS and add docs
* Make flags more flexible to support disabling system site packages
* Merge pull request `#14 <https://github.com/locusrobotics/catkin_virtualenv/issues/14>`_ from locusrobotics/fix-pip
  Fix issues due to pip 10 release
* Review comments
* Lock down pip version
* Make logging optional
* Contributors: Paul Bovbel

0.1.6 (2018-01-10)
------------------
* Re-enable pip upgrade
* Contributors: Paul Bovbel

0.1.5 (2018-01-10)
------------------
* Disable pip upgrade
* Drop strict requirements
* Update package.xml
* Contributors: Paul Bovbel

0.1.4 (2017-12-03)
------------------
* Fixup CMake and local directory cleanup
* Merge pull request `#9 <https://github.com/locusrobotics/catkin_virtualenv/issues/9>`_ from locusrobotics/python3-compat
  Python 3 compatiblity tweaks
* Add base requirements file for python3 catkin; include extra data about requirement merge failure
* Fix cmake lint errors
* Add XML schema, README badges, fix travis config for debian jessie, and remove legacy scripts
* Contributors: Paul Bovbel

0.1.3 (2017-11-27)
------------------
* Simplify install path
* Clean up vars
* Instantiate both a devel- and install-space venv
* Contributors: Paul Bovbel

0.1.2 (2017-11-23)
------------------
* Drop rosbash dependency and move python scripts into cmake directory
* More tweaks to get nosetests working in python3
* Contributors: Paul Bovbel

0.1.1 (2017-11-22)
------------------
* Fixup module path
* Contributors: Paul Bovbel

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
