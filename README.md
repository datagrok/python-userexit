# UserExit

Letting expected exceptions bubble up to end your script with a Python traceback is scary and unhelpful for users. But sprinkling `sys.exit("error message")` all over your script is ugly, and can be troublesome for testing or importing.

Tidy up with custom exception classes! Even for simple scripts, it's worth the trouble. (And it's less trouble than you think!)

This repository provides a small Python class to make it even easier to adopt this pattern.

## Features

- Built-in decorator enables handler with a single line of code.
- Messages are automatically whitespace-stripped and wrapped, to declutter source code.
- Messages are automatically `.format()`ed with the custom class arguments and 'self'
- (TODO) A bit of metaclass magic makes each of your error classes automatically set its own unique exit status, unless you explicitly assign one.

## License: AGPL-3.0+

All of the code herein is copyright 2016 [Michael F. Lamb](http://datagrok.org) and released under the terms of the [GNU Affero General Public License, version 3][AGPL-3.0+] (or, at your option, any later version.)

[AGPL-3.0+]: http://www.gnu.org/licenses/agpl.html
