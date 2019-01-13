import unittest
import userexit


class FooExit(userexit.UserExit):
    # will inherit UserExit's status 0
    message = "FooExit"


class FooAbort(userexit.UserAbort):
    exit_status = 80
    message = "FooAbort"


class BarAbort(userexit.UserAbort):
    # will be auto-assigned exit status 79
    message = "BarAbort"


class BarAbortVariant(BarAbort):
    # will inherit BarAbort's exit status 79
    message = "A specific type of BarAbort"


class BarAbortVariantB(BarAbort):
    exit_status = 85
    message = "A specific type of BarAbort B"


class BarAbortVariantC(BarAbort, userexit.UserAbort):
    # will be auto-assigned exit status 81
    message = "A specific type of BarAbort C"


class BazAbort(userexit.UserAbort):
    # will be auto-assigned exit status 82
    message = "BazAbort"


class QuxAbort(userexit.UserAbort):
    # not a good choice, can be confused with shell's "command not found"
    # but we don't crash if the user insists to use it
    exit_status = 127
    message = "QuxAbort"


class UserExitTestCase(unittest.TestCase):

    def test_exit_status_builtins(self):
        # These shouldn't change no matter what subclasses we create
        self.assertEqual(userexit.UserExit.exit_status, 0)
        self.assertEqual(userexit.UserAbort.exit_status, 1)

    def test_exit_status_userexit_subclass(self):
        # subclasses of UserExit (end without error) get status 0
        self.assertEqual(FooExit.exit_status, 0)

    def test_exit_status_manual_assignment(self):
        # You can manually assign any exit status
        self.assertEqual(FooAbort.exit_status, 80)
        # even one outside the "safe" pool
        self.assertEqual(QuxAbort.exit_status, 127)

    def test_exit_status_automatic_assignment(self):
        # Subclasses of UserExit that don't specify one get auto-assigned an
        # exit status
        self.assertEqual(BarAbort.exit_status, 79)

    def test_exit_status_parent_assignment_subclass(self):
        # Subclasses of Subclasses of UserExit get the same exit status as
        # their parent
        self.assertEqual(BarAbortVariant.exit_status, 79)

    def test_exit_status_manual_assignment_subclass(self):
        # if you don't want Subclass of Subclass to get the same exit status as
        # its parent, you can specify one explicitly
        self.assertEqual(BarAbortVariantB.exit_status, 85)

    def test_exit_status_automatic_assignment_subclass(self):
        # if you don't want Subclass of Subclass to get the same exit status as
        # its parent, you can put UserExit in the list of subclasses to force
        # auto-assignment
        self.assertEqual(BarAbortVariantC.exit_status, 81)

    def test_exit_status_automatic_assignment_skips_used(self):
        # When we manually assign, it gets removed from the available pool
        self.assertEqual(BazAbort.exit_status, 82)

    def test_instances_exit_status_same_as_class(self):
        # no new exit status should be assigned or generated when a class is
        # instantiated
        self.assertEqual(userexit.UserExit().exit_status, 0)
        self.assertEqual(userexit.UserAbort().exit_status, 1)
        self.assertEqual(FooExit().exit_status, 0)
        self.assertEqual(BazAbort().exit_status, 82)
