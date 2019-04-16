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

from packaging.requirements import InvalidRequirement


class VcsRequirement(object):
    '''A non-semver requirement from a version control system.
    eg. svn+http://myrepo/svn/MyApp#egg=MyApp
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
        self.string = string

        match = self.name_regex.search(self.string)
        if match is None:
            raise InvalidRequirement("No match for {}".format(self.name_regex.pattern))

        self.name = match.group('name')
        if self.name is None:
            raise InvalidRequirement("No project name '#egg=<name>' was provided")

    def __str__(self):
        return self.string
