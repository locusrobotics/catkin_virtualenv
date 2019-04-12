# Software License Agreement (GPL)
#
# \file      requirements.py
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
import re

from copy import copy
from enum import Enum
from functools import total_ordering


@total_ordering
class SemVer(object):
    version_regex = re.compile("^[0-9\.]+$")

    def __init__(self, string):
        # type: (str) -> None
        if not self.version_regex.match(string):
            raise RuntimeError("Invalid requirement version {}, must match {}".format(
                string, self.version_regex.pattern))

        self._version = [int(v) for v in string.split('.')]

    def __eq__(self, other):
        # type: (SemVer, SemVer) -> bool
        return self._version == other._version

    def __lt__(self, other):
        # type: (SemVer, SemVer) -> bool
        return self._version < other._version

    def __str__(self):
        # type: (SemVer) -> str
        return '.'.join([str(v) for v in self._version])


class ReqType(Enum):
    GREATER = ">="
    EXACT = "=="
    ANY = None


class ReqMergeException(RuntimeError):
    def __init__(self, req, other):
        # type: (Requirement, Requirement) -> None
        self.req = req
        self.other = other

    def __str__(self):
        # type: () -> str
        return "Cannot merge requirements {} and {}".format(self.req, self.other)


class VcsRequirement(object):
    '''A non-semver requirement from a version control system.
    eg. svn+http://myrepo/svn/MyApp#egg=MyApp

    I'm reimplementing the Requirement class below, but it looks like we don't use it. So maybe some of this
    reimplementation is unnecessary. Instead we might want to be reimplementing `packaging.Requirement`
    '''

    # Borrowing https://github.com/pypa/pipenv/tree/dde2e52cb8bc9bfca7af6c6b1a4576faf00e84f1/pipenv/vendor/requirements
    VCS_SCHEMES = [
        'git',
        'git+https',
        'git+ssh',
        'git+git',
        'hg+http',
        'hg+https',
        'hg+static-http',
        'hg+ssh',
        'svn',
        'svn+svn',
        'svn+http',
        'svn+https',
        'svn+ssh',
        'bzr+http',
        'bzr+https',
        'bzr+ssh',
        'bzr+sftp',
        'bzr+ftp',
        'bzr+lp',
    ]

    name_regex = re.compile(
        r'^(?P<scheme>{0})://'.format(r'|'.join(
            [scheme.replace('+', r'\+') for scheme in VCS_SCHEMES])) +
        r'((?P<login>[^/@]+)@)?'
        r'(?P<path>[^#@]+)'
        r'(@(?P<revision>[^#]+))?'
        r'(#egg=(?P<name>[^&]+))?$'
    )

    def __init__(self, string):
        self.name = string

        if not self.name_regex.match(string):
            raise RuntimeError("Invalid VCS requirement name {}, must match {}".format(string, self.name_regex))

    def __str__(self):
        return self.name

    def __add__(self, other):
        # Not sure where this gets used. Because we don't do versions it may be safe to just always return self.
        return copy(self)


class Requirement(object):
    name_regex = re.compile("^[][A-Za-z0-9._-]+$")

    def __init__(self, string):
        # type: (str) -> None
        for operation in [ReqType.GREATER, ReqType.EXACT, ReqType.ANY]:
            fields = string.split(operation.value)
            if len(fields) > 1:
                break

        self.name = fields[0].lower()
        if not self.name_regex.match(self.name):
            raise RuntimeError("Invalid requirement name {}, must match {}".format(
                string, self.name_regex.pattern))

        self.operation = operation
        try:
            self.version = SemVer(fields[1])
        except IndexError:
            self.version = None

    def __str__(self):
        # type: () -> str
        return "{}{}{}".format(
            self.name,
            self.operation.value if self.operation.value else "",
            self.version if self.version else ""
        )

    def __add__(self, other):
        # type: (Requirement) -> Requirement
        if self.name != other.name:
            raise ReqMergeException(self, other)

        operation_map = {
            self.operation: self,
            other.operation: other,
        }
        operation_set = set(operation_map)

        if operation_set == {ReqType.EXACT}:
            if self.version == other.version:
                return copy(self)
            else:
                raise ReqMergeException(self, other)

        elif operation_set == {ReqType.EXACT, ReqType.GREATER}:
            if operation_map[ReqType.EXACT].version >= operation_map[ReqType.GREATER].version:
                return copy(operation_map[ReqType.EXACT])
            else:
                raise ReqMergeException(self, other)

        elif operation_set == {ReqType.GREATER}:
            out = copy(operation_map[ReqType.GREATER])
            out.version = max(self.version, other.version)
            return out

        elif ReqType.ANY in operation_set:
            if len(operation_set) == 1:
                return copy(self)
            else:
                out = copy(self)
                out.operation = (operation_set - {ReqType.ANY}).pop()
                out.version = operation_map[out.operation].version
                return out
