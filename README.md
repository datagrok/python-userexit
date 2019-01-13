# UserExit / UserAbort

Letting expected exceptions bubble up to end your Python script with a traceback is scary and unhelpful for users.
But sprinkling `sys.exit("error message")` all over your script is ugly, and can be troublesome for testing or importing.
And when you want to provide a clear, verbose error message, even `raise ValueError("A long message {} with {} some {} interpolated {} values".format(foo, bar, baz, qux))` can easily exceed your preferred line length and clutter your logic.

Tidy up with custom exception classes!
Even for simple scripts, it's worth the trouble.
(And it's less trouble than you think!)

This repository provides a small Python class to make it easy to adopt this pattern.

## Example

Create subclasses of `UserAbort` (for errors) or `UserExit` (for normal, successful termination) and set their `message` appropriately.

```python
from userexit import UserExit, UserAbort

class BadInputError(UserAbort):
    message = """
        Input {} should be set to {}, please adjust
        your settings and re-run {sys.argv[0]}.
        """

class TargetFileMissingError(UserAbort):
    message = "Please ensure the target file {} exists."
```

Replace verbose error messages and calls to sys.exit in your code with nice concise `raise` statements.

```python
...
class...:
    def...:
        ...
        if input != expected:
            raise BadInputError(input, expected)
        ...
        try:
            with open(filename) as fh:
                ...
        except FileNotFoundError:
            raise TargetFileMissingError(filename)
        ...
```

Then, decorate your main method with `@UserExit.handle`.

```python
@UserExit.handle
def main():
        ...

if __name__ == '__main__':
    main()
```

For deeper exploration of the theory of operation, see [DESIGN.md](DESIGN.md).

## Features

- Built-in decorator enables handler with a single line of code.
- Messages are automatically whitespace-stripped and wrapped, to declutter source code.
- Messages are automatically `.format()`ed with the custom class arguments and 'self'
- A bit of metaclass magic makes each of your error classes automatically set its own unique exit status, unless you explicitly assign one.

## License: AGPL-3.0+

All of the code herein is copyright 2019 [Michael F. Lamb](http://datagrok.org) and released under the terms of the [GNU Affero General Public License, version 3][AGPL-3.0+] (or, at your option, any later version.)

[AGPL-3.0+]: http://www.gnu.org/licenses/agpl.html
