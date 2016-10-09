"""userexit.py

Defines an exception superclass UserExit for easy creation of custom
exceptions that abort execution with an error message but no traceback.

See README.md for usage and theory of operation.

"""
#
# Copyright 2016  Michael F. Lamb <http://datagrok.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# License: AGPL-3.0+ http://www.gnu.org/licenses/agpl.html
#

import functools
import sys
import textwrap


def format_script(s):
    """Helper that unindents multiline docstrings."""
    return textwrap.dedent(s).strip() + '\n'


def format_msg(s):
    """Helper that unwraps dedented multiline multi-paragraph
    strings."""
    return '\n\n'.join(
            para if '>>>' in para else textwrap.fill(para)
            for para in s.split('\n\n'))


class UserExit(Exception):
    exit_status = 0
    message = "Execution ended normally."
    prefix_name = True
    prefix_error = True

    @staticmethod
    def handle(fn):
        @functools.wraps(fn)
        def inner(*args, **kwargs):
            try:
                fn(*args, **kwargs)
            except UserExit as ex:
                print(ex)
                raise SystemExit(ex.exit_status)
        return inner

    def __str__(self):
        message = ""
        if self.prefix_name:
            message += "{argv[0]}: "
        if self.prefix_error and self.exit_status != 0:
            message += "error: "
        message += format_script(self.message)
        return format_msg(
                message.format(*self.args, self=self, argv=sys.argv))


class UserAbort(UserExit):
    exit_status = 1
    message = "Execution aborted with an error."
    prefix_error = False