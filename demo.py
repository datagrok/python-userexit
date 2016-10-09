from userexit import UserExit


class BadInputError(UserExit):
    exit_status = 3
    message = """
        Input {!r} should be set to {!r}. Please adjust your settings
        and re-run {argv[0]!r}.
        """


class TargetFileMissingError(UserExit):
    exit_status = 4
    message = "Please ensure the target file {} exists."


class MyClass(object):
    """A dummy class to demonstrate UserExit."""

    def a_method(self, x):
        y = False
        if x != y:
            raise BadInputError(x, y)

        filename = 'this_file_does_not_exist.txt'
        try:
            with open(filename) as fh:
                print(fh.read())
        except FileNotFoundError:
            raise TargetFileMissingError(filename)


@UserExit.handle
def main():
    c = MyClass()
    c.a_method(True)

if __name__ == '__main__':
    main()
