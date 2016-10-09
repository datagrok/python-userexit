# UserExit

Letting expected exceptions bubble up to end your script with a Python traceback is scary and unhelpful for users. But sprinkling `sys.exit("error message")` all over your script is ugly, and can be troublesome for testing or importing.

Tidy up with custom exception classes! Even for simple scripts, it's worth the trouble. (And it's less trouble than you think!)

This repository provides a small Python class to make it even easier to adopt this pattern.

## Example

Wrap your main method with `@UserExit.handle`. Then create subclasses of `UserExit` and set their `message` appropriately.

    import UserExit
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


    @UserExit.handle
    def main():
            ...

    if __name__ == '__main__':
        main()

Elsewhere, in the same or different module:

    class BadInputError(UserExit):
        exit_status = 3
        message = """
            Input {} should be set to {}, please adjust
            your settings and re-run {sys.argv[0]}.
            """

    class TargetFileMissingError(UserExit):
        exit_status = 4
        message = "Please ensure the target file {} exists."

## Features

- Built-in decorator enables handler with a single line of code.
- Messages are automatically whitespace-stripped and wrapped, to declutter source code.
- Messages are automatically `.format()`ed with the custom class arguments and 'self'
- (TODO) A bit of metaclass magic makes each of your error classes automatically set its own unique exit status, unless you explicitly assign one.

## License: AGPL-3.0+

All of the code herein is copyright 2016 [Michael F. Lamb](http://datagrok.org) and released under the terms of the [GNU Affero General Public License, version 3][AGPL-3.0+] (or, at your option, any later version.)

[AGPL-3.0+]: http://www.gnu.org/licenses/agpl.html
