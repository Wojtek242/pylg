# -----------------------------------------------------------------------------
# PyLg: module to facilitate and automate the process of writing runtime logs.
# Copyright (C) 2017 Wojciech Kozlowski <wojciech.kozlowski@vivaldi.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# -----------------------------------------------------------------------------

from datetime import datetime
from functools import partial
import traceback
import warnings
import textwrap
import inspect
import sys
import os

# -----------------------------------------------------------------------------
# Load settings.
# -----------------------------------------------------------------------------
from .loadSettings import *


class ClassNameStack(object):

    """ A class to keep a global stack of the class names of the
        functions that are currently executing. The class name of the
        last traced function that was called will be on top of the
        stack. It is removed after it finishes executing.
    """

    stack = []

    @staticmethod
    def insert(classname):
        if CLASS_NAME_RESOLUTION:
            ClassNameStack.stack.append(classname)

    @staticmethod
    def pop():
        if CLASS_NAME_RESOLUTION and ClassNameStack.stack:
                ClassNameStack.stack.pop()

    @staticmethod
    def get():
        if CLASS_NAME_RESOLUTION and ClassNameStack.stack:
            return ClassNameStack.stack[-1]
        else:
            return None


class PyLg(object):

    """ Class to handle the log file.
    """

    wfile = None
    filename = PYLG_FILE

    @staticmethod
    def set_filename(new_filename):

        """ Change the file name of the log file. The change will be
            rejected if the log file is already open.

            :param str new_filename: The new file name for the log file.
        """

        if PyLg.wfile is None:
            PyLg.filename = new_filename
        else:
            warnings.warn("PyLg wfile is open - cannot change filename")

    @staticmethod
    def write(string):

        """ Write to the log file. A new log file is opened and
            initialised if it has not been opened yet.

            :param str string: The string to be written to the log file.
        """

        if PyLg.wfile is None:
            PyLg.wfile = open(PyLg.filename, "w")
            PyLg.wfile.write("=== Log initialised at " +
                             str(datetime.now()) + " ===\n\n")

        PyLg.wfile.write(string)
        PyLg.wfile.flush()

    @staticmethod
    def close():

        """ Close the log file.
        """

        if PyLg.wfile is not None:
            PyLg.wfile.close()
            PyLg.wfile = None
        else:
            warnings.warn("PyLg wfile is not open - nothing to close")


class TraceFunction(object):

    """ Class that serves as a decorator to trace entry and exit from
        functions. Used by appending @TraceFunction on top of the
        definition of the function to trace.
    """

    class TraceFunctionStruct(object):

        """ Internal object to handle traced function properties.
        """

        function = None
        varnames = None
        defaults = None

        filename = None
        lineno = None
        classname = None
        functionname = None

    def __get__(self, obj, objtype):

        """ Support for instance functions.
        """

        return partial(self.__call__, obj)

    def __init__(self, *args, **kwargs):

        """ Constructor for TraceFunction. Note that the behaviour is
            different depending on whether TraceFunction is passed any
            parameters. For details see __call__ in this class.
        """

        # ---------------------------------------------------------------------
        # Make sure this decorator is never called with no arguments.
        # ---------------------------------------------------------------------
        assert args or kwargs

        if args:

            self.trace_args = DEFAULT_TRACE_ARGS
            self.trace_rv = DEFAULT_TRACE_RV

            # -----------------------------------------------------------------
            # The function init_function will verify the input.
            # -----------------------------------------------------------------
            self.init_function(*args, **kwargs)

        if kwargs:

            trace_args_str = 'trace_args'
            trace_rv_str = 'trace_rv'

            # -----------------------------------------------------------------
            # If kwargs is non-empty, it should only contain trace_rv,
            # trace_args, or both and args should be empty. Assert all
            # this.
            # -----------------------------------------------------------------
            assert not args
            assert (len(kwargs) > 0) and (len(kwargs) <= 2)
            if len(kwargs) == 1:
                assert (trace_rv_str in kwargs) or (trace_args_str in kwargs)
            elif len(kwargs) == 2:
                assert (trace_rv_str in kwargs) and (trace_args_str in kwargs)

            if trace_args_str in kwargs:
                self.trace_args = kwargs[trace_args_str]
            else:
                self.trace_args = DEFAULT_TRACE_ARGS

            if trace_rv_str in kwargs:
                self.trace_rv = kwargs[trace_rv_str]
            else:
                self.trace_rv = DEFAULT_TRACE_RV

            self.function = None

    def __call__(self, *args, **kwargs):

        """ The actual wrapper that is called when a call to a
            decorated function is made. It also handles extra
            initialisation when parameters are passed to
            TraceFunction.

            :return: The return value of the decorated function.
        """

        # ---------------------------------------------------------------------
        # __call__ has to behave differently depending on whether the
        # decorator has been given any parameters. The reason for this
        # is as follows:
        #
        # @TraceFunction
        # decorated_function
        #
        # translates to TraceFunction(decorated_function)
        #
        # @TraceFunction(*args, **kwargs)
        # decorated_function
        #
        # translates to TraceFunction(*args, **kwargs)(decorated_function)
        #
        # In both cases, the result should be a callable object which
        # will be called whenever the decorated function is called. In
        # the first case, the callable object is an instance of
        # TraceFunction, in the latter case the return value of
        # TraceFunction.__call__ is the callable object.
        # ---------------------------------------------------------------------

        if self.function is None:
            # -----------------------------------------------------------------
            # If the decorator has been passed a parameter, __init__
            # will not define self.function and __call__ will be
            # called immediately after __init__ with the decorated
            # function as the only parameter. Therefore, this __call__
            # function has to return the callable object that is meant
            # to be called every time the decorated function is
            # called. Here, self is returned in order to return the
            # object as the callable handle for the decorated
            # function. This if block should be hit only once at most
            # and only during initialisation.
            # -----------------------------------------------------------------
            self.init_function(*args, **kwargs)
            return self

        # ---------------------------------------------------------------------
        # The actual decorating.
        # ---------------------------------------------------------------------
        ClassNameStack.insert(self.function.classname)
        self.trace_entry(*args, **kwargs)

        try:
            rv = self.function.function(*args, **kwargs)
        except Exception as e:
            self.trace_exception(e)

            if EXCEPTION_EXIT:
                traceback.print_exc(file=sys.stderr)
                os._exit(1)

            raise

        self.trace_exit(rv)
        ClassNameStack.pop()

        return rv

    def init_function(self, *args, **kwargs):

        """ Function to initialise the TraceFunctionStruct kept by the
            decorator.
        """

        # ---------------------------------------------------------------------
        # This function should only ever be called with one parameter
        # - the function to be decorated. These checks are done here,
        # rather than by the caller, as anything that calls this
        # function should also have been called with the decorated
        # function as its only parameter.
        # ---------------------------------------------------------------------
        assert not kwargs
        assert len(args) == 1
        assert callable(args[0])

        self.function = TraceFunction.TraceFunctionStruct()

        self.function.function = args[0]

        argspec = inspect.getargspec(self.function.function)

        self.function.varnames = argspec.args
        if argspec.defaults is not None:
            self.function.defaults = dict(
                zip(argspec.args[-len(argspec.defaults):],
                    argspec.defaults))

        # ---------------------------------------------------------------------
        # init_function is called from either __init__ or __call__ and
        # we want the frame before that.
        # ---------------------------------------------------------------------
        frames_back = 2
        caller_frame = inspect.stack()[frames_back]

        self.function.filename = os.path.basename(caller_frame[1])
        self.function.lineno = caller_frame[2]
        self.function.classname = caller_frame[3]
        self.function.functionname = self.function.function.__name__

    def trace_entry(self, *args, **kwargs):

        """ Called on function entry. This function collects all the
            function arguments and constructs a message to pass to
            trace.
        """

        # ---------------------------------------------------------------------
        # The ENTRY message.
        # ---------------------------------------------------------------------
        msg = "-> ENTRY"
        if args or kwargs:
            msg += ": "

            n_args = len(args)
            if self.trace_args:
                for arg in range(n_args):

                    if not TRACE_SELF and \
                       self.function.varnames[arg] == "self":
                        continue

                    msg += (self.function.varnames[arg] + " = " +
                            self.get_value_string(args[arg]) + ", ")

                for name in self.function.varnames[n_args:]:
                    msg += name + " = "
                    if name in kwargs:
                        value = kwargs[name]
                    else:
                        value = self.function.defaults[name]
                    msg += self.get_value_string(value) +  ", "

                msg = msg[:-2]

            else:
                msg += "---"

        trace(msg, function=self.function)

    def trace_exit(self, rv=None):

        """ Called on function exit to log the fact that a function has
            finished executing.

            :param rv: The return value of the traced function.
        """

        # ---------------------------------------------------------------------
        # The EXIT message.
        # ---------------------------------------------------------------------
        msg = "<- EXIT "
        if rv is not None:
            msg += ": "
            if self.trace_rv:
                msg += self.get_value_string(rv)
            else:
                msg += "---"

        trace(msg, function=self.function)
        return

    def trace_exception(self, exception):

        """ Called when a function terminated due to an exception.

            :param exception: The raised exception.
        """

        # ---------------------------------------------------------------------
        # The EXIT message.
        # ---------------------------------------------------------------------
        core_msg = type(exception).__name__ + " RAISED"
        msg = "<- EXIT : " + core_msg

        if str(exception) is not "":
            msg += " - " + str(exception)

        if EXCEPTION_WARNING:
            warnings.warn(core_msg, RuntimeWarning)

        trace(msg, function=self.function)
        return

    def get_value_string(self, value):

        """ Convert value to a string for the log.
        """

        if isinstance(value, list) and COLLAPSE_LISTS:
            return self.collapse_list(value)
        elif isinstance(value, dict) and COLLAPSE_DICTS:
            return self.collapse_dict(value)
        else:
            return str(value)

    def collapse_list(self, ll):
        return "[ len=" + str(len(ll)) + " ]"

    def collapse_dict(self, dd):
        return "{ len=" + str(len(dd)) + " }"


def trace(message, function=None):

    """ Writes message to the log file. It will also log the time,
        filename, line number and function name.

        :param str message: The log message.
        :param function: A TraceFunctionStruct object if called from within
                         TraceFunction.
    """

    if function is None:
        # ---------------------------------------------------------------------
        # If there is no function object, we need to work out
        # where the trace call was made from.
        # ---------------------------------------------------------------------
        frames_back = 1
        caller_frame = inspect.stack()[frames_back]

        filename = os.path.basename(caller_frame[1])
        lineno = caller_frame[2]
        functionname = caller_frame[3]

    else:
        filename = function.filename
        lineno = function.lineno
        functionname = function.functionname

    # -------------------------------------------------------------------------
    # If CLASS_NAME_RESOLUTION is enabled, the top element of the
    # stack should be the class name of the function from which this
    # trace call is made. This cannot be policed so the user must make
    # sure this is the case by ensuring that trace is only called
    # outside of any function or from within functions that have the
    # @TraceFunction decorator.
    # -------------------------------------------------------------------------
    classname = ClassNameStack.get()
    if classname is not None and classname != "<module>":
        functionname = classname + "." + functionname

    # -------------------------------------------------------------------------
    # Generate the string based on the settings.
    # -------------------------------------------------------------------------
    msg = ""

    if TRACE_TIME:
        msg += datetime.now().strftime(TIME_FORMAT) + "  "

    if TRACE_FILENAME:
        msg += '{filename:{w}.{w}}  '.format(filename=filename,
                                             w=FILENAME_COLUMN_WIDTH)

    if TRACE_LINENO:
        msg += '{lineno:0{w}}: '.format(lineno=lineno, w=LINENO_WIDTH)

    if TRACE_FUNCTION:
        msg += '{function:{w}.{w}}  '.format(function=functionname,
                                             w=FUNCTION_COLUMN_WIDTH)

    if TRACE_MESSAGE:

        message = str(message)

        if MESSAGE_WIDTH > 0:

            # -----------------------------------------------------------------
            # Get the length of the trace line so far
            # -----------------------------------------------------------------
            premsglen = len(msg)

            # -----------------------------------------------------------------
            # Wrap the text.
            # -----------------------------------------------------------------
            wrapped = textwrap.wrap(message, MESSAGE_WIDTH)

            if wrapped:
                if MESSAGE_WRAP:

                    # ---------------------------------------------------------
                    # Print the first line. It gets special treatment
                    # as it doesn't need whitespace in front of it.
                    # ---------------------------------------------------------
                    msg += wrapped[0]

                    # ---------------------------------------------------------
                    # Print the remaining lines. Append whitespace to
                    # align it with the first line.
                    # ---------------------------------------------------------
                    for line in wrapped[1:]:
                        msg += '\n' + '{:{w}}'.format('', w=premsglen) + line

                else:
                    # ---------------------------------------------------------
                    # The message is not being wrapped.
                    # ---------------------------------------------------------

                    if MESSAGE_MARK_TRUNCATION and wrapped[1:]:
                        # -----------------------------------------------------
                        # We want to mark truncated lines so we need
                        # to determine if the line is being
                        # truncated. If it is we replace the last
                        # character with '\'.
                        # -----------------------------------------------------

                        if MESSAGE_WIDTH > 1:
                            wrapped = textwrap.wrap(wrapped[0],
                                                    MESSAGE_WIDTH - 1)
                            assert wrapped

                            msg += ('{m:{w}}'.format(m=wrapped[0],
                                                     w=MESSAGE_WIDTH - 1) +
                                    '\\')

                        else:
                            assert MESSAGE_WIDTH == 1
                            msg += '\\'

                    else:
                        # -----------------------------------------------------
                        # Either the message is not being truncated or
                        # MESSAGE_MARK_TRUNCATION is False.
                        # -----------------------------------------------------
                        msg += wrapped[0]

        else:
            # -----------------------------------------------------------------
            # A MESSAGE_WIDTH of 0 denotes no limit.
            # -----------------------------------------------------------------
            assert MESSAGE_WIDTH == 0
            msg += message

    # -------------------------------------------------------------------------
    # Terminate the log line with a newline.
    # -------------------------------------------------------------------------
    msg += "\n"

    # -------------------------------------------------------------------------
    # Write the data to the log file.
    # -------------------------------------------------------------------------
    PyLg.write(msg)
