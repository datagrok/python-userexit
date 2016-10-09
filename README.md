# UserExit

Letting expected exceptions bubble up to end your script with a Python traceback is scary and unhelpful for users. But sprinkling `sys.exit("error message")` all over your script is ugly, and can be troublesome for testing or importing.

Tidy up with custom exception classes! Even for simple scripts, it's worth the trouble. (And it's less trouble than you think!)

This repository provides a small Python class to make it even easier to adopt this pattern.

## Example

<table width=100%><tr><th>Instead of this</th><th>write this</th></tr><tr><td>

    import sys


    class...:

        def...:
            ...
            if input != expected:
                print("Input {} should be set to {},"
                      " please adjust your settings"
                      " and re-run {}."
                      .format(input,
                              expected,
                              sys.argv[0]))
                sys.exit(3)
            ...
            try:
                with open(filename) as fh:
                    ...
            except FileNotFoundError:
                print("Please ensure the target file"
                      " {} exists.".format(filename))
                sys.exit(4)
            ...


    def main():
            ...
    
    if __name__ == '__main__':
        main()

</td><td>

    import UserExit
    

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

</td></tr><tr><td>
</td><td>

    # elsewhere in the same or different module...

    class BadInputError(UserExit):
        exit_status = 3
        message = """
            Input {} should be set to {}, please adjust
            your settings and re-run {sys.argv[0]}.
            """

    class TargetFileMissingError(UserExit):
        exit_status = 4
        message = """
            Please ensure the target file {} exists.
            """

</td></tr></table>
<table width=100%><tr><th>Before</th><th>After</th></tr><tr><td>

</td><td>

    from userexit import UserExit

</td></tr><tr><td>

    def logic(foo):
        if f:
            raise SystemExit(
                "{} is not a valid"
                " option".format(option))



</td><td>

    def logic():
        if f:
            raise BadOption(option)

    @UserExit.handle
    def main():
 
    if __name__ == '__main__':
        main()

</td></tr><tr><td>

</td><td>

    class NormalUserExit(UserExit):
        code = 0
        message = None
    class UserAbortedExit(UserExit):
        message = "Aborted by user."
    class UserAbortedExit(UserExit):
        message = "Aborted by user."
    class BadOption(UserExit):
        message = """
            {} is not a valid option.
            """

</td></tr></table>

## Features

- Built-in decorator enables handler with a single line of code.
- A bit of metaclass magic makes each of your error classes automatically set its own unique exit status, unless you explicitly assign one.
- Messages are automatically whitespace-stripped and wrapped, to declutter source code.
- Messages are automatically `.format()`ed with the custom class arguments and 'self'

## Rationale

Simple scripts for use at the command line often have expected failure modes: the input is nonsensical, a file is missing, the environment isn't the way we expect, etc. In those situations, we want to:

1. abort execution immediately
2. show a message to the user
3. set an error exit status, and
4. avoid showing a Python traceback.

It's simple enough to do this in a naive way that clutters our source code, but with very little extra effort we can do it in an elegant and maintainable way instead.

### The naive way

When we do this in the naive way, it usually looks like this:

    if <an exceptional case occured>:
        raise SystemExit(<a message for the user>)

If we want to produce a useful error message, we might format the message with values from variables. The length of the code to craft a good message may easily span more than one line of source code. Furthermore, if we're handling an exception that exists within multiple levels of indentation, the line length we have left to work with is reduced.

Using `SystemExit` in this way always sets an exit status of 1. This indicates an error, but does not allow wrapping scripts to determine what kind of error occurred. What if we want to exit with a different status code? What if we want to exit without an error, but with a message? Then, our code becomes:

    if <an exceptional case occured>:
        print(<a message for the user>)
        raise SystemExit(<a numeric exit status>)

The error status we pass to `SystemExit` serves as an interface for any scripts that invoke ours, so they can appropriately respond to failures. So, well-written scripts should assign unique exit statuses to each class of problem encountered, and should not change in future versions of our script. We have to keep track of the mapping between numeric status and the type of problem in our script.




This code pattern must be sprinkled throughout our otherwise straightforward logic. If the same error situation might occur multiple places, we might repeat code blocks verbatim with copy and paste rather than take the trouble to factor it out.


When writing shell script, we usually deal with those situations by printing an error message and calling "exit" to abort the script. "Die with an error."

Algorithms are easier to read and understand when you can focus on the usual-case logic in the main body, and move the handling of exceptional cases elsewhere.

Sometimes, you'll end up needing to report the same fatal error message from multiple locations in your script. Copy-pasting `raise SystemExit("A long error message")` everywhere needed is ugly, can lead to typos, increases maintenance burden.

When you want to display an error and set a specific exit status, the situation is worse: not one but multiple lines of code mixed into your otherwise clear and straightforward logic. UserExit 

Error messages intended for users to read are sometimes 

What if you or someone else wants to localize your script, so that its messages will appear in the user's configured language? Applying localization mechanisms throughout your code is further clutter.

Calls to `sys.exit` or `SystemExit` from the functions that your script uses will cause problems if anyone tries to import your script to use as a library. Allowing Python's exception mechanism to abort your program gives other programmers the opportunity to intercept and react to errors.

    # shell script example
    if [ ! -f $1 ]; then
        # die with an error
        echo >&2 "Error: the specified file does not exist: $1"
        exit 2
    fi

    [ -d "/var/run/foo/$2" ] || {
        echo >&2 "Error: the specified cluster is invalid: $2"
        exit 3
    }

    # Python example

### Clever alternatives that don't work

- Overloading the custom exception's docstring to contain the error message: breaks if Python is launched with `-OO` or `PYTHONOPTIMIZE=2` (which removes docstrings) is set in the environment.

- Using `assert` instead of `if` to check for exceptional cases and throw an exception on failure. Again, `-O` or `PYTHONOPTIMIZE` set nonzero break this, since optimization elides asserts.

## License: AGPL-3.0+

All of the code herein is copyright 2016 [Michael F. Lamb](http://datagrok.org) and released under the terms of the [GNU Affero General Public License, version 3][AGPL-3.0+] (or, at your option, any later version.)

[AGPL-3.0+]: http://www.gnu.org/licenses/agpl.html
