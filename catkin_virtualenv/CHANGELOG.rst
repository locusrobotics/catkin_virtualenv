^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changelog for package catkin_virtualenv
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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
