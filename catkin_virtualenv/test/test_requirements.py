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

from catkin_virtualenv.requirements import parse_requirement, parse_requirements, Requirement, InvalidRequirement


class TestRequirements(unittest.TestCase):

    def test_requirement_parse(self):
        string = "asdf"
        req = parse_requirement(string)
        self.assertEqual(req.name, "asdf")

    def test_vcs_requirement_parse(self):
        string = "git+git://github.com/pytransitions/transitions@dev-async#egg=transitions"
        req = parse_requirement(string)
        self.assertEqual(req.name, "transitions")

    def test_requirement_parse_no_name(self):
        string = "git+git://github.com/pytransitions/transitions@dev-async"
        with self.assertRaises(InvalidRequirement):
            _ = parse_requirement(string)

    def test_requirements_parse(self):
        requirements_text = """
            # comment
            ## more comment
            package_one
            package_two==1.0.0 # this is a comment
            git+git://github.com/pytransitions/transitions@dev-async#egg=transitions
            # even more comments
        """
        requirements = {
            "package_one",
            "package_two==1.0.0",
            "git+git://github.com/pytransitions/transitions@dev-async#egg=transitions",
        }

        parsed = parse_requirements(requirements_text)
        self.assertEqual({str(req) for req in parsed}, requirements)
