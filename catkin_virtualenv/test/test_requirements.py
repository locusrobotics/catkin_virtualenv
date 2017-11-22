# Software License Agreement (GPL)
#
# \file      test_requirements.py
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
import unittest

from catkin_virtualenv.requirements import Requirement, SemVer


class TestRequirements(unittest.TestCase):

    def test_string_transform(self):
        reqs = [
            "module",
            "module>=0.0.5",
            "module==1.0.5",
        ]

        for req in reqs:
            self.assertEqual(str(Requirement(req)), req)

    def test_failed_transform(self):
        reqs = [
            "$$asdfasdf",
            "module$==1.0.5",
            "module>=0.a.5",
            "module===1.0.5",
            "module=1.0.5",
        ]

        for req in reqs:
            with self.assertRaises(RuntimeError) as cm:
                print(Requirement(req))
            print(cm.exception)

    def test_addition(self):
        reqs = [
            ("module==1.0.0",   "module",      "module==1.0.0"),
            ("module==1.1.0",   "module>=0.4", "module==1.1.0"),
            ("module==1.2.0",   "module>=0.8", "module==1.2.0"),
            ("module",          "module",      "module"),
            ("module>=0.5",     "module",      "module>=0.5"),
            ("module>=0.3",     "module>=10.0.8", "module>=10.0.8"),
        ]

        for req in reqs:
            #  Check addition both ways for commutation
            for direction in ((0, 1), (1, 0)):
                left = Requirement(req[direction[0]])
                right = Requirement(req[direction[1]])
                result = left + right
                self.assertEqual(str(result), req[2])

                # Make sure we're returning a new object from the addition method
                self.assertIsNot(right, result)
                self.assertIsNot(left, result)

    def test_failed_addition(self):
        reqs = [
            ("module==1.0.0",   "module==2.0.0"),
            ("module==1.0.0",   "module>=1.0.4"),
            ("module==1.0.0",   "other_module"),
            ("module",          "other_module"),
        ]

        for req in reqs:
            with self.assertRaises(RuntimeError) as cm:
                print(Requirement(req[0]) + Requirement(req[1]))
            print(cm.exception)


class TestSemVer(unittest.TestCase):

    def test_comparison(self):
        versions = [
            ("1.0.0",   "0"),
            ("3.0.0",   "0.1"),
            ("1.0.0",   "0.1.1.1.1.1"),
            ("4.0.0",   "0.1234.1"),
            ("44.0.0",  "003.12"),
            ("0.5",     "0.0.4"),
            ("0.0.5",   "0.0.4"),
            ("1.22.3",  "1.002.3"),
            ("1.10.0",  "1.9.0"),
        ]
        for version in versions:
            self.assertTrue(SemVer(version[0]) > SemVer(version[1]))
