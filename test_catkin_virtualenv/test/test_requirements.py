import unittest

from locus_py.requirements import Requirement, SemVer


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
