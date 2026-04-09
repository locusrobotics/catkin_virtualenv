# catkin_virtualenv Test Packages

This directory contains test packages for verifying catkin_virtualenv functionality.

## Test Packages

| Package | Description |
|---------|-------------|
| `test_catkin_virtualenv` | Basic virtualenv functionality test. Verifies that pip packages are installed and importable. |
| `test_catkin_virtualenv_distro_codename` | Tests distro-specific requirements files (e.g., `requirements-jammy.txt`). Verifies the correct lockfile is selected based on the OS codename. |
| `test_catkin_virtualenv_inherited` | Tests requirement inheritance. Verifies that a package inherits pip requirements from its catkin dependencies, and can override versions. |
| `test_catkin_virtualenv_isolated` | Tests `ISOLATE_REQUIREMENTS TRUE`. Verifies that pip requirements from catkin dependencies are **not** inherited when isolation is enabled. |
| `test_catkin_virtualenv_no_system_packages` | Tests `USE_SYSTEM_PACKAGES FALSE`. Verifies that system-installed Python packages (via apt) are **not** visible inside the virtualenv. |
