^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changelog for package catkin_virtualenv
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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
