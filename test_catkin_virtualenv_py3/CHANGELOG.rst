^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changelog for package test_catkin_virtualenv_py3
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

0.5.1 (2019-08-19)
------------------

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
* Merge pull request `#31 <https://github.com/locusrobotics/catkin_virtualenv/issues/31>`_ from locusrobotics/add-extra-pip-args
  Clean up extra_pip_args PR
* Contributors: Paul Bovbel, Shingo Kitagawa

0.2.1 (2018-06-04)
------------------

0.2.0 (2018-05-03)
------------------
* Merge pull request `#16 <https://github.com/locusrobotics/catkin_virtualenv/issues/16>`_ from locusrobotics/system-site-packages
  Provide more CMake flags to customize behaviour
* Implement ISOLATE_REQUIREMENTS and add docs
* Contributors: Paul Bovbel

0.1.6 (2018-01-10)
------------------

0.1.5 (2018-01-10)
------------------
* Drop strict requirements
* Contributors: Paul Bovbel

0.1.4 (2017-12-03)
------------------
* Merge pull request `#9 <https://github.com/locusrobotics/catkin_virtualenv/issues/9>`_ from locusrobotics/python3-compat
  Python 3 compatiblity tweaks
* Add base requirements file for python3 catkin; include extra data about requirement merge failure
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
* Contributors: Paul Bovbel
