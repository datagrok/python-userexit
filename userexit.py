"""userexit.py

Defines an exception superclass UserExit for easy creation of custom
exceptions that abort execution with an error message but no traceback.

See README.md for usage and theory of operation.

"""
#
# Copyright 2019  Michael F. Lamb <http://datagrok.org>
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

from __future__ import print_function

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


def _usable_statuses():
    """Helper for SetDefaultExitStatus.

    Return a list of exit statuses that are "safe" to use, in reverse order.


    From https://www.tldp.org/LDP/abs/html/exitcodes.html#EXITCODESREF :

    "... exit codes 1--2, 126--165, and 255 have special meanings, and should
    therefore be avoided for user-specified exit parameters."

    "usr/include/sysexits.h allocates previously unused exit codes from 64--78.
    [Using these] should not cause any problems, since there is no overlap or
    conflict in usage of exit codes between compiled C/C++ binaries and shell
    scripts."

    "The author of this document proposes restricting user-defined exit codes
    to the range 64--113 to conform with the C/C++ standard."

    So we assign, in order of preference:
        79--113, as recommended by that author,
        64--78, which that author says "should not cause problems,"
        3--63, 114--125, 166--254, neither recommended by that author nor
        mentioned in the table of special meanings,
        1, when all others are used.
    """
    ranges = [
        range(79, 114),
        range(64, 79),
        range(3, 64),
        range(114, 126),
        range(166, 255)]
    lst = list(x for r in ranges for x in r)
    # .reverse() because .pop() might be more efficient than .pop(0)
    lst.reverse()
    return lst


class SetDefaultExitStatus(type):
    """Metaclass. Sets class attribute "exit_status" when unspecified.

    Each subclass of UserAbort will be assigned a different exit status from a
    pool of "safe to use" statuses until the pool is exhausted, at which point
    they will be assigned exit status 1.
    """

    def __new__(cls, name, bases, dct, _statuses=_usable_statuses()):
        if 'exit_status' in dct:
            try:
                _statuses.remove(dct['exit_status'])
            except ValueError:
                pass
        elif UserAbort in bases:
            try:
                dct['exit_status'] = _statuses.pop()
            except IndexError:
                dct['exit_status'] = 1
        return super().__new__(cls, name, bases, dct)


class UserExit(Exception):
    exit_status = 0
    message = "Execution ended normally."
    prefix_name = True
    prefix_error = True

    @classmethod
    def handle(kls, fn):
        """Decorator that will handle this exception.

        Typical use is to decorate your main function.

        Example: this causes any subclasses of UserExit raised within
        main() to be handled appropriately: a message is printed for the
        user with no Python traceback, and execution ends with a nonzero
        exit status:

            @UserExit.handle
            def main():
                ...

            if __name__ == "__main__":
                main()

        Each subclass of UserExit contains this class method; using it
        from a subclass will handle only that class of exception.

        """
        @functools.wraps(fn)
        def inner(*args, **kwargs):
            try:
                fn(*args, **kwargs)
            except kls as ex:
                print(ex, file=sys.stderr)
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


class UserAbort(UserExit, metaclass=SetDefaultExitStatus):
    exit_status = 1
    message = "Execution aborted with an error."
    prefix_error = False


# @userexit.handle decorator
handle = UserExit.handle
