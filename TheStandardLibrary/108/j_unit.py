#!/usr/bin/env python
'''
Python unit testing framework, based on Erich Gamma's JUnit and Kent Beck's
Smalltalk testing framework.

This module contains the core framework classes that form the basis of
specific test cases and suites (TestCase, TestSuite etc.), and also a
text-based utility class for running the tests and reporting the results
 (TextTestRunner).

Simple usage:

    import unit_test

    class IntegerArithmenticTestCase(unit_test.TestCase):
        def test_add(self):  ## test method names begin 'test*'
            self.assert_equals((1 + 2), 3)
            self.assert_equals(0 + 1, 1)
        def test_multiply(self):
            self.assert_equals((0 * 10), 0)
            self.assert_equals((5 * 8), 40)

    if __name__ == '__main__':
        unit_test.main()

Further information is available in the bundled documentation, and from

  http://docs.python.org/lib/module-unit_test.html

Copyright (c) 1999-2003 Steve Purcell
This module is free software, and you may redistribute it and/or modify
it under the same terms as Python itself, so long as this copyright message
and disclaimer are retained in their original form.

IN NO EVENT SHALL THE AUTHOR BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT,
SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE USE OF
THIS CODE, EVEN IF THE AUTHOR HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH
DAMAGE.

THE AUTHOR SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
PARTICULAR PURPOSE.  THE CODE PROVIDED HEREUNDER IS ON AN "AS IS" BASIS,
AND THERE IS NO OBLIGATION WHATSOEVER TO PROVIDE MAINTENANCE,
SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS.
'''

__author__ = "Steve Purcell"
__email__ = "stephen_purcell at yahoo dot com"
__version__ = "#Revision: 1.63 $"[11:-2]
'''
import time
import sys
import traceback
import os
import types

##############################################################################
# Exported classes and functions
##############################################################################
__all__ = ['TestResult', 'TestCase', 'TestSuite', 'TextTestRunner',
           'TestLoader', 'FunctionTestCase', 'main', 'default_test_loader']

# Expose obsolete functions for backwards compatibility
__all__.extend(['get_test_case_names', 'make_suite', 'find_test_cases'])


##############################################################################
# Backward compatibility
##############################################################################

def _CmpToKey(mycmp):
    'Convert a cmp= function into a key= function'
    class K(object):
        def __init__(self, obj):
            self.obj = obj
        def __lt__(self, other):
            return mycmp(self.obj, other.obj) == -1
    return K

##############################################################################
# Test framework core
##############################################################################

def _strclass(cls):
    return "%s.%s" % (cls.__module__, cls.__name__)

__unittest = 1

class TestResult(object):
    """Holder for test result information.

    Test results are automatically managed by the TestCase and TestSuite
    classes, and do not need to be explicitly manipulated by writers of tests.

    Each instance holds the total number of tests run, and collections of
    failures and errors that occurred among those test runs. The collections
    contain tuples of (testcase, exceptioninfo), where exceptioninfo is the
    formatted traceback of the error that occurred.
    """
    def __init__(self):
        self.failures = []
        self.errors = []
        self.tests_run = 0
        self.should_stop = False

    def start_test(self, test):
        "Called when the given test is about to be run"
        self.tests_run = self.tests_run + 1

    def stop_test(self, test):
        "Called when the given test has been run"
        pass

    def add_error(self, test, err):
        """Called when an error has occurred. 'err' is a tuple of values as
        returned by sys.exc_info().
        """
        self.errors.append((test, self._exc_info_to_string(err, test)))

    def add_failure(self, test, err):
        """Called when an error has occurred. 'err' is a tuple of values as
        returned by sys.exc_info()."""
        self.failures.append((test, self._exc_info_to_string(err, test)))

    def add_success(self, test):
        "Called when a test has completed successfully"
        pass

    def was_successful(self):
        "Tells whether or not this result was a success"
        return len(self.failures) == len(self.errors) == 0

    def stop(self):
        "Indicates that the tests should be aborted"
        self.should_stop = True

    def _exc_info_to_string(self, err, test):
        """Converts a sys.exc_info()-style tuple of values into a string."""
        exctype, value, tb = err
        # Skip test runner traceback levels
        while tb and self._is_relevant_tb_level(tb):
            tb = tb.tb_next
        if exctype is test.failure_exception:
            # Skip assert*() traceback levels
            length = self._count_relevant_tb_levels(tb)
            return ''.join(traceback.format_exception(exctype, value, tb, length))
        return ''.join(traceback.format_exception(exctype, value, tb))

    def _is_relevant_tb_level(self, tb):
        return '__unittest' in tb.tb_frame.f_globals

    def _count_relevant_tb_levels(self, tb):
        length = 0
        while tb and not self._is_relevant_tb_level(tb):
            length += 1
            tb = tb.tb_next
        return length

    def __repr__(self):
        return "<%s run=%i errors=%i failures=%i>" % \
               (_strclass(self.__class__), self.tests_run, len(self.errors),
                len(self.failures))

class AssertRaisesContext(object):
    def __init__(self, expected, test_case):
        self.expected = expected
        self.failure_exception = test_case.failure_exception
    def __enter__(self):
        pass
    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            try:
                exc_name = self.expected.__name__
            except AttributeError:
                exc_name = str(self.expected)
            raise self.failure_exception(
                "{0} not raised".format(exc_name))
        if issubclass(exc_type, self.expected):
            return True
        # Let unexpected exceptions skip through
        return False

class TestCase(object):
    """A class whose instances are single test cases.

    By default, the test code itself should be placed in a method named
    'run_test'.

    If the fixture may be used for many test cases, create as
    many test methods as are needed. When instantiating such a TestCase
    subclass, specify in the constructor arguments the name of the test method
    that the instance is to execute.

    Test authors should subclass TestCase for their own tests. Construction
    and deconstruction of the test's environment ('fixture') can be
    implemented by overriding the 'set_up' and 'tear_down' methods respectively.

    If it is necessary to override the __init__ method, the base class
    __init__ method must always be called. It is important that subclasses
    should not change the signature of their __init__ method, since instances
    of the classes are instantiated automatically by parts of the framework
    in order to be run.
    """

    # This attribute determines which exception will be raised when
    # the instance's assertion methods fail; test methods raising this
    # exception will be deemed to have 'failed' rather than 'errored'

    failure_exception = AssertionError

    def __init__(self, method_name='run_test'):
        """Create an instance of the class that will use the named test
           method when executed. Raises a ValueError if the instance does
           not have a method with the specified name.
        """
        try:
            self._test_method_name = method_name
            test_method = getattr(self, method_name)
            self._test_method_doc = test_method.__doc__
        except AttributeError:
            raise ValueError("no such test method in %s: %s" % \
                  (self.__class__, method_name))

    def set_up(self):
        "Hook method for setting up the test fixture before exercising it."
        pass

    def tear_down(self):
        "Hook method for deconstructing the test fixture after testing it."
        pass

    def count_test_cases(self):
        return 1

    def default_test_result(self):
        return TestResult()

    def short_description(self):
        """Returns a one-line description of the test, or None if no
        description has been provided.

        The default implementation of this method returns the first line of
        the specified test method's docstring.
        """
        doc = self._test_method_doc
        return doc and doc.split("\n")[0].strip() or None

    def id(self):
        return "%s.%s" % (_strclass(self.__class__), self._test_method_name)

    def __eq__(self, other):
        if type(self) is not type(other):
            return False

        return self._test_method_name == other._test_method_name

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((type(self), self._test_method_name))

    def __str__(self):
        return "%s (%s)" % (self._test_method_name, _strclass(self.__class__))

    def __repr__(self):
        return "<%s test_method=%s>" % \
               (_strclass(self.__class__), self._test_method_name)

    def run(self, result=None):
        if result is None: result = self.default_test_result()
        result.start_test(self)
        test_method = getattr(self, self._test_method_name)
        try:
            try:
                self.set_up()
            except Exception:
                result.add_error(self, self._exc_info())
                return

            ok = False
            try:
                test_method()
                ok = True
            except self.failure_exception:
                result.add_failure(self, self._exc_info())
            except Exception:
                result.add_error(self, self._exc_info())

            try:
                self.tear_down()
            except Exception:
                result.add_error(self, self._exc_info())
                ok = False
            if ok: result.add_success(self)
        finally:
            result.stop_test(self)

    def __call__(self, *args, **kwds):
        return self.run(*args, **kwds)

    def debug(self):
        """Run the test without collecting errors in a TestResult"""
        self.set_up()
        getattr(self, self._test_method_name)()
        self.tear_down()

    def _exc_info(self):
        """Return a version of sys.exc_info() with the traceback frame
           minimised; usually the top level of the traceback frame is not
           needed.
        """
        return sys.exc_info()

    def fail(self, msg=None):
        """Fail immediately, with the given message."""
        raise self.failure_exception(msg)

    def fail_if(self, expr, msg=None):
        "Fail the test if the expression is true."
        if expr: raise self.failure_exception(msg)

    def fail_unless(self, expr, msg=None):
        """Fail the test unless the expression is true."""
        if not expr: raise self.failure_exception(msg)

    def fail_unless_raises(self, exc_class, callable_obj=None, *args, **kwargs):
        """Fail unless an exception of class exc_class is thrown
           by callable_obj when invoked with arguments args and keyword
           arguments kwargs. If a different type of exception is
           thrown, it will not be caught, and the test case will be
           deemed to have suffered an error, exactly as for an
           unexpected exception.

           If called with callable_obj omitted or None, will return a
           context object used like this::

                with self.fail_unless_raises(some_error_class):
                    do_something()
        """
        context = AssertRaisesContext(exc_class, self)
        if callable_obj is None:
            return context
        with context:
            callable_obj(*args, **kwargs)

    def fail_unless_equal(self, first, second, msg=None):
        """Fail if the two objects are unequal as determined by the '=='
           operator.
        """
        if not first == second:
            raise self.failure_exception(msg or '%r != %r' % (first, second))

    def fail_if_equal(self, first, second, msg=None):
        """Fail if the two objects are equal as determined by the '=='
           operator.
        """
        if first == second:
            raise self.failure_exception(msg or '%r == %r' % (first, second))

    def fail_unless_almost_equal(self, first, second, places=7, msg=None):
        """Fail if the two objects are unequal as determined by their
           difference rounded to the given number of decimal places
           (default 7) and comparing to zero.

           Note that decimal places (from zero) are usually not the same
           as significant digits (measured from the most signficant digit).
        """
        if round(abs(second-first), places) != 0:
            raise self.failure_exception(
                  msg or '%r != %r within %r places' % (first, second, places))

    def fail_if_almost_equal(self, first, second, places=7, msg=None):
        """Fail if the two objects are equal as determined by their
           difference rounded to the given number of decimal places
           (default 7) and comparing to zero.

           Note that decimal places (from zero) are usually not the same
           as significant digits (measured from the most signficant digit).
        """
        if round(abs(second-first), places) == 0:
            raise self.failure_exception(
                  msg or '%r == %r within %r places' % (first, second, places))

    # Synonyms for assertion methods

    assert_equal = assert_equals = fail_unless_equal

    assert_not_equal = assert_not_equals = fail_if_equal

    assert_almost_equal = assert_almost_equals = fail_unless_almost_equal

    assert_not_almost_equal = assert_not_almost_equals = fail_if_almost_equal

    assert_raises = fail_unless_raises

    assert_ = assert_true = fail_unless

    assert_false = fail_if



class TestSuite(object):
    """A test suite is a composite test consisting of a number of TestCases.

    For use, create an instance of TestSuite, then add test case instances.
    When all tests have been added, the suite can be passed to a test
    runner, such as TextTestRunner. It will run the individual test cases
    in the order in which they were added, aggregating the results. When
    subclassing, do not forget to call the base class constructor.
    """
    def __init__(self, tests=()):
        self._tests = []
        self.add_tests(tests)

    def __repr__(self):
        return "<%s tests=%s>" % (_strclass(self.__class__), self._tests)

    __str__ = __repr__

    def __eq__(self, other):
        if type(self) is not type(other):
            return False
        return self._tests == other._tests

    def __ne__(self, other):
        return not self == other

    # Can't guarantee hash invariant, so flag as unhashable
    __hash__ = None

    def __iter__(self):
        return iter(self._tests)

    def count_test_cases(self):
        cases = 0
        for test in self._tests:
            cases += test.count_test_cases()
        return cases

    def add_test(self, test):
        # sanity checks
        if not hasattr(test, '__call__'):
            raise TypeError("the test to add must be callable")
        if (isinstance(test, (type, types.ClassType)) and
            issubclass(test, (TestCase, TestSuite))):
            raise TypeError("TestCases and TestSuites must be instantiated "
                            "before passing them to add_test()")
        self._tests.append(test)

    def add_tests(self, tests):
        if isinstance(tests, basestring):
            raise TypeError("tests must be an iterable of tests, not a string")
        for test in tests:
            self.add_test(test)

    def run(self, result):
        for test in self._tests:
            if result.should_stop:
                break
            test(result)
        return result

    def __call__(self, *args, **kwds):
        return self.run(*args, **kwds)

    def debug(self):
        """Run the tests without collecting errors in a TestResult"""
        for test in self._tests: test.debug()


class FunctionTestCase(TestCase):
    """A test case that wraps a test function.

    This is useful for slipping pre-existing test functions into the
    unit_test framework. Optionally, set-up and tidy-up functions can be
    supplied. As with TestCase, the tidy-up ('tear_down') function will
    always be called if the set-up ('set_up') function ran successfully.
    """

    def __init__(self, test_func, set_up=None, tear_down=None,
                 description=None):
        TestCase.__init__(self)
        self.__setUpFunc = set_up
        self.__tearDownFunc = tear_down
        self.__testFunc = test_func
        self.__description = description

    def set_up(self):
        if self.__setUpFunc is not None:
            self.__setUpFunc()

    def tear_down(self):
        if self.__tearDownFunc is not None:
            self.__tearDownFunc()

    def run_test(self):
        self.__testFunc()

    def id(self):
        return self.__testFunc.__name__

    def __eq__(self, other):
        if type(self) is not type(other):
            return False

        return self.__setUpFunc == other.__setUpFunc and \
               self.__tearDownFunc == other.__tearDownFunc and \
               self.__testFunc == other.__testFunc and \
               self.__description == other.__description

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((type(self), self.__setUpFunc, self.__tearDownFunc,
                                           self.__testFunc, self.__description))

    def __str__(self):
        return "%s (%s)" % (_strclass(self.__class__), self.__testFunc.__name__)

    def __repr__(self):
        return "<%s test_func=%s>" % (_strclass(self.__class__), self.__testFunc)

    def short_description(self):
        if self.__description is not None: return self.__description
        doc = self.__testFunc.__doc__
        return doc and doc.split("\n")[0].strip() or None



##############################################################################
# Locating and loading tests
##############################################################################

class TestLoader(object):
    """This class is responsible for loading tests according to various
    criteria and returning them wrapped in a TestSuite
    """
    test_method_prefix = 'test'
    sort_test_methods_using = cmp
    suite_class = TestSuite

    def load_tests_from_test_case(self, test_case_class):
        """Return a suite of all tests cases contained in test_case_class"""
        if issubclass(test_case_class, TestSuite):
            raise TypeError("Test cases should not be derived from TestSuite. Maybe you meant to derive from TestCase?")
        test_case_names = self.get_test_case_names(test_case_class)
        if not test_case_names and hasattr(test_case_class, 'run_test'):
            test_case_names = ['run_test']
        return self.suite_class(map(test_case_class, test_case_names))

    def load_tests_from_module(self, module):
        """Return a suite of all tests cases contained in the given module"""
        tests = []
        for name in dir(module):
            obj = getattr(module, name)
            if (isinstance(obj, (type, types.ClassType)) and
                issubclass(obj, TestCase)):
                tests.append(self.load_tests_from_test_case(obj))
        return self.suite_class(tests)

    def load_tests_from_name(self, name, module=None):
        """Return a suite of all tests cases given a string specifier.

        The name may resolve either to a module, a test case class, a
        test method within a test case class, or a callable object which
        returns a TestCase or TestSuite instance.

        The method optionally resolves the names relative to a given module.
        """
        parts = name.split('.')
        if module is None:
            parts_copy = parts[:]
            while parts_copy:
                try:
                    module = __import__('.'.join(parts_copy))
                    break
                except ImportError:
                    del parts_copy[-1]
                    if not parts_copy: raise
            parts = parts[1:]
        obj = module
        for part in parts:
            parent, obj = obj, getattr(obj, part)

        if isinstance(obj, types.ModuleType):
            return self.load_tests_from_module(obj)
        elif (isinstance(obj, (type, types.ClassType)) and
              issubclass(obj, TestCase)):
            return self.load_tests_from_test_case(obj)
        elif (isinstance(obj, types.UnboundMethodType) and
              isinstance(parent, (type, types.ClassType)) and
              issubclass(parent, TestCase)):
            return TestSuite([parent(obj.__name__)])
        elif isinstance(obj, TestSuite):
            return obj
        elif hasattr(obj, '__call__'):
            test = obj()
            if isinstance(test, TestSuite):
                return test
            elif isinstance(test, TestCase):
                return TestSuite([test])
            else:
                raise TypeError("calling %s returned %s, not a test" %
                                (obj, test))
        else:
            raise TypeError("don't know how to make test from: %s" % obj)

    def load_tests_from_names(self, names, module=None):
        """Return a suite of all tests cases found using the given sequence
        of string specifiers. See 'load_tests_from_name()'.
        """
        suites = [self.load_tests_from_name(name, module) for name in names]
        return self.suite_class(suites)

    def get_test_case_names(self, test_case_class):
        """Return a sorted sequence of method names found within test_case_class
        """
        def is_test_method(attrname, test_case_class=test_case_class, prefix=self.test_method_prefix):
            return attrname.startswith(prefix) and hasattr(getattr(test_case_class, attrname), '__call__')
        test_fn_names = filter(is_test_method, dir(test_case_class))
        if self.sort_test_methods_using:
            test_fn_names.sort(key=_CmpToKey(self.sort_test_methods_using))
        return test_fn_names



default_test_loader = TestLoader()


##############################################################################
# Patches for old functions: these functions should be considered obsolete
##############################################################################

def _make_loader(prefix, sort_using, suite_class=None):
    loader = TestLoader()
    loader.sort_test_methods_using = sort_using
    loader.test_method_prefix = prefix
    if suite_class: loader.suite_class = suite_class
    return loader

def get_test_case_names(test_case_class, prefix, sort_using=cmp):
    return _make_loader(prefix, sort_using).get_test_case_names(test_case_class)

def make_suite(test_case_class, prefix='test', sort_using=cmp, suite_class=TestSuite):
    return _make_loader(prefix, sort_using, suite_class).load_tests_from_test_case(test_case_class)

def find_test_cases(module, prefix='test', sort_using=cmp, suite_class=TestSuite):
    return _make_loader(prefix, sort_using, suite_class).load_tests_from_module(module)


##############################################################################
# Text UI
##############################################################################

class _WritelnDecorator(object):
    """Used to decorate file-like objects with a handy 'writeln' method"""
    def __init__(self,stream):
        self.stream = stream

    def __getattr__(self, attr):
        return getattr(self.stream,attr)

    def writeln(self, arg=None):
        if arg: self.write(arg)
        self.write('\n') # text-mode streams translate to \r\n if needed


class _TextTestResult(TestResult):
    """A test result class that can print formatted text results to a stream.

    Used by TextTestRunner.
    """
    separator1 = '=' * 70
    separator2 = '-' * 70

    def __init__(self, stream, descriptions, verbosity):
        TestResult.__init__(self)
        self.stream = stream
        self.show_all = verbosity > 1
        self.dots = verbosity == 1
        self.descriptions = descriptions

    def get_description(self, test):
        if self.descriptions:
            return test.short_description() or str(test)
        else:
            return str(test)

    def start_test(self, test):
        TestResult.start_test(self, test)
        if self.show_all:
            self.stream.write(self.get_description(test))
            self.stream.write(" ... ")
            self.stream.flush()

    def add_success(self, test):
        TestResult.add_success(self, test)
        if self.show_all:
            self.stream.writeln("ok")
        elif self.dots:
            self.stream.write('.')
            self.stream.flush()

    def add_error(self, test, err):
        TestResult.add_error(self, test, err)
        if self.show_all:
            self.stream.writeln("ERROR")
        elif self.dots:
            self.stream.write('E')
            self.stream.flush()

    def add_failure(self, test, err):
        TestResult.add_failure(self, test, err)
        if self.show_all:
            self.stream.writeln("FAIL")
        elif self.dots:
            self.stream.write('F')
            self.stream.flush()

    def print_errors(self):
        if self.dots or self.show_all:
            self.stream.writeln()
        self.print_error_list('ERROR', self.errors)
        self.print_error_list('FAIL', self.failures)

    def print_error_list(self, flavour, errors):
        for test, err in errors:
            self.stream.writeln(self.separator1)
            self.stream.writeln("%s: %s" % (flavour,self.get_description(test)))
            self.stream.writeln(self.separator2)
            self.stream.writeln("%s" % err)


class TextTestRunner(object):
    """A test runner class that displays results in textual form.

    It prints out the names of tests as they are run, errors as they
    occur, and a summary of the results at the end of the test run.
    """
    def __init__(self, stream=sys.stderr, descriptions=1, verbosity=1):
        self.stream = _WritelnDecorator(stream)
        self.descriptions = descriptions
        self.verbosity = verbosity

    def _make_result(self):
        return _TextTestResult(self.stream, self.descriptions, self.verbosity)

    def run(self, test):
        "Run the given test case or test suite."
        result = self._make_result()
        start_time = time.time()
        test(result)
        stop_time = time.time()
        time_taken = stop_time - start_time
        result.print_errors()
        self.stream.writeln(result.separator2)
        run = result.tests_run
        self.stream.writeln("Ran %d test%s in %.3fs" %
                            (run, run != 1 and "s" or "", time_taken))
        self.stream.writeln()
        if not result.was_successful():
            self.stream.write("FAILED (")
            failed, errored = map(len, (result.failures, result.errors))
            if failed:
                self.stream.write("failures=%d" % failed)
            if errored:
                if failed: self.stream.write(", ")
                self.stream.write("errors=%d" % errored)
            self.stream.writeln(")")
        else:
            self.stream.writeln("OK")
        return result



##############################################################################
# Facilities for running tests from the command line
##############################################################################

class TestProgram(object):
    """A command-line program that runs a set of tests; this is primarily
       for making test modules conveniently executable.
    """
    USAGE = """\
Usage: %(prog_name)s [options] [test] [...]

Options:
  -h, --help       Show this message
  -v, --verbose    Verbose output
  -q, --quiet      Minimal output

Examples:
  %(prog_name)s                               - run default set of tests
  %(prog_name)s MyTestSuite                   - run suite 'MyTestSuite'
  %(prog_name)s MyTestCase.test_something      - run MyTestCase.test_something
  %(prog_name)s MyTestCase                    - run all 'test*' test methods
                                               in MyTestCase
"""
    def __init__(self, module='__main__', default_test=None,
                 argv=None, test_runner=TextTestRunner,
                 test_loader=default_test_loader):
        if isinstance(module, basestring):
            self.module = __import__(module)
            for part in module.split('.')[1:]:
                self.module = getattr(self.module, part)
        else:
            self.module = module
        if argv is None:
            argv = sys.argv
        self.verbosity = 1
        self.default_test = default_test
        self.test_runner = test_runner
        self.test_loader = test_loader
        self.prog_name = os.path.basename(argv[0])
        self.parse_args(argv)
        self.run_tests()

    def usage_exit(self, msg=None):
        if msg: print msg
        print self.USAGE % self.__dict__
        sys.exit(2)

    def parse_args(self, argv):
        import getopt
        try:
            options, args = getopt.getopt(argv[1:], 'h_hvq',
                                          ['help','verbose','quiet'])
            for opt, value in options:
                if opt in ('-h','-H','--help'):
                    self.usage_exit()
                if opt in ('-q','--quiet'):
                    self.verbosity = 0
                if opt in ('-v','--verbose'):
                    self.verbosity = 2
            if len(args) == 0 and self.default_test is None:
                self.test = self.test_loader.load_tests_from_module(self.module)
                return
            if len(args) > 0:
                self.test_names = args
            else:
                self.test_names = (self.default_test,)
            self.create_tests()
        except getopt.error, msg:
            self.usage_exit(msg)

    def create_tests(self):
        self.test = self.test_loader.load_tests_from_names(self.test_names,
                                                       self.module)

    def run_tests(self):
        if isinstance(self.test_runner, (type, types.ClassType)):
            try:
                test_runner = self.test_runner(verbosity=self.verbosity)
            except TypeError:
                # didn't accept the verbosity argument
                test_runner = self.test_runner()
        else:
            # it is assumed to be a TestRunner instance
            test_runner = self.test_runner
        result = test_runner.run(self.test)
        sys.exit(not result.was_successful())

main = TestProgram


##############################################################################
# Executing this module from the command line
##############################################################################

if __name__ == "__main__":
    main(module=None)
'''