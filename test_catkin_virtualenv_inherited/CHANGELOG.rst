^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changelog for package test_catkin_virtualenv
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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
