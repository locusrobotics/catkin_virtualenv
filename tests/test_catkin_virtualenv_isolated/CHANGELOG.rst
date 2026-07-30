^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changelog for package test_catkin_virtualenv_isolated
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Forthcoming
-----------

0.19.0 (2026-06-18)
-------------------
* Use nose-py3 and restore tests around isolated and system package flags (#125)
  * Consume a codenamed lockfile when available, to make building across different distributions more straightforward
  * Fix tests in test_catkin_virtualenv_distro_codename
  * Fix tests by removing requests due to six complexity; use attrs instead
  * Turns out six is just a very bad marker package
  * Use nose-py3 and restore test_catkin_virtualenv_isolated
  * Fix isolated build test and flag processing
  * Fix tests and isolated build functionality
  * Remove stray CHANGELOG files
* Contributors: Paul Bovbel
