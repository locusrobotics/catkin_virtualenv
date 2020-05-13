# -*- coding: utf-8 -*-
# Copyright (c) 2013 - 2014 Spotify AB

# This file is part of dh-virtualenv.

# dh-virtualenv is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 2 of the
# License, or (at your option) any later version.

# dh-virtualenv is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with dh-virtualenv. If not, see
# <http://www.gnu.org/licenses/>.

def _find_script_files(self):
    """Find list of files containing python shebangs in the bin directory. """
    command = ['grep', '-l', '-r',
                '-e', r'^#!.*bin/\(env \)\?{0}'.format(_PYTHON_INTERPRETERS_REGEX),
                '-e', r"^'''exec.*bin/{0}".format(_PYTHON_INTERPRETERS_REGEX),
                os.path.join(self.path, 'bin')]
    grep_proc = subprocess.Popen(command, stdout=subprocess.PIPE)
    files, _ = grep_proc.communicate()
    return set(f for f in files.decode('utf-8').strip().split('\n') if f)

def _fix_shebangs(self, target_dir):
    """Translate /usr/bin/python and /usr/bin/env python shebang
    lines to point to our virtualenv python.
    """
    pythonpath = os.path.join(target_dir, 'bin/python')
    for f in self._find_script_files():
        regex = (
            r's-^#!.*bin/\(env \)\?{names}\"\?-#!{pythonpath}-;'
            r"s-^'''exec'.*bin/{names}-'''exec' {pythonpath}-"
        ).format(names=_PYTHON_INTERPRETERS_REGEX, pythonpath=re.escape(pythonpath))
        check_call(['sed', '-i', regex, f])

def _fix_activate_path(self, target_dir):
    """Replace the `VIRTUAL_ENV` path in bin/activate to reflect the
    post-install path of the virtualenv.
    """
    activate_settings = [
        [
            'VIRTUAL_ENV="{0}"'.format(target_dir),
            r'^VIRTUAL_ENV=.*$',
            "activate"
        ],
        [
            'setenv VIRTUAL_ENV "{0}"'.format(target_dir),
            r'^setenv VIRTUAL_ENV.*$',
            "activate.csh"
        ],
        [
            'set -gx VIRTUAL_ENV "{0}"'.format(target_dir),
            r'^set -gx VIRTUAL_ENV.*$',
            "activate.fish"
        ],
    ]

    for activate_args in activate_settings:
        virtualenv_path = activate_args[0]
        pattern = re.compile(activate_args[1], flags=re.M)
        activate_file = activate_args[2]

        with open(self._venv_bin(activate_file), 'r+') as fh:
            content = pattern.sub(virtualenv_path, fh.read())
            fh.seek(0)
            fh.truncate()
            fh.write(content)

def _fix_local_symlinks(self):
    # The virtualenv might end up with a local folder that points outside the package
    # Specifically it might point at the build environment that created it!
    # Make those links relative
    # See https://github.com/pypa/virtualenv/commit/5cb7cd652953441a6696c15bdac3c4f9746dfaa1
    local_dir = os.path.join(self.path, "local")
    if not os.path.isdir(local_dir):
        return
    elif os.path.samefile(self.path, local_dir):
        # "local" points directly to its containing directory
        os.unlink(local_dir)
        os.symlink(".", local_dir)
        return

    for d in os.listdir(local_dir):
        path = os.path.join(local_dir, d)
        if not os.path.islink(path):
            continue

        existing_target = os.readlink(path)
        if not os.path.isabs(existing_target):
            # If the symlink is already relative, we don't
            # want to touch it.
            continue

        new_target = os.path.relpath(existing_target, local_dir)
        os.unlink(path)
        os.symlink(new_target, path)
