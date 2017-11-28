^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changelog for package catkin_virtualenv
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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
