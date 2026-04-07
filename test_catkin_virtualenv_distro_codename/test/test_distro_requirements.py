# Software License Agreement (GPL)
#
# \file      test_distro_requirements.py
# \authors   Paul Bovbel <pbovbel@locusrobotics.com>
# \copyright Copyright (c) (2017,), Locus Robotics, All rights reserved.
#
# This program is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 2 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
import distro
import importlib
import unittest


class TestDistroRequirements(unittest.TestCase):
    """Test that distro-specific requirements files are used correctly."""

    def test_distro_specific_package_version(self):
        """
        Verify that the correct requirements file was used based on distro.

        - On Jammy: six==1.17.0 (from requirements-jammy.txt)
        - On Noble: six==1.18.0 (from requirements-noble.txt)
        - On other distros: six==1.16.0 (from requirements.txt)
        """
        six = importlib.import_module("six")
        codename = distro.codename().lower()

        expected_versions = {
            "jammy": "1.17.0",
            "noble": "1.18.0",
        }
        expected = expected_versions.get(codename, "1.16.0")

        self.assertEqual(
            six.__version__,
            expected,
            f"Expected six {expected} on {codename}, got {six.__version__}",
        )


if __name__ == "__main__":
    unittest.main()
