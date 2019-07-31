"""PyLg: facilitate and automate the process of writing runtime logs."""

from datetime import datetime
from functools import partial
from typing import Optional
import traceback
import warnings
import textwrap
import inspect
import sys
import os

from pylg.settings import _pylg_check_bool
import pylg.settings


class ClassNameStack:
    """Stack for the class names of the currently executing functions.

    The class name of the last traced function that was called will be on top
    of the stack. It is removed after it finishes executing.

    """

    stack = []

    @classmethod
    def disable(cls) -> None:
        """Disable the stack.

        This is achieved by rendering all functions no-ops.

        WARNING: This is an irreversible operation.

        """
        cls.insert = lambda _classname: None
        cls.pop = lambda: None
        cls.get = lambda: None

    @classmethod
    def insert(cls, classname: str) -> None:
        """Insert an entry.

        Parameters
        ----------
        classname : str
            The class name to insert.

        """
        cls.stack.append(classname)

    @classmethod
    def pop(cls) -> str:
        """str: Return top-most entry and remove it."""
        return cls.stack.pop() if cls.stack else None

    @classmethod
    def peek(cls) -> str:
        """str: Return the top-most entry without removing it."""
        return ClassNameStack.stack[-1] if cls.stack else None


class PyLg:
    """Class to handle the log file."""

    wfile = None

    @classmethod
    def configure(cls, user_settings_path: Optional[str] = None) -> None:
        """PyLg initialisation.

        Parameters
        ----------
        user_settings_path : Optional[str]
            Path to the user settings file.

        """

        # ---------------------------------------------------------------------
        # Load the settings.
        # ---------------------------------------------------------------------
        settings = pylg.settings.load(user_settings_path)

        # ---------------------------------------------------------------------
        # Local variables for settings to avoid dictionary access which is only
        # O(1) on average. Admittedly the size of the settings dict is not
        # large, but these accesses will be frequent.
        # ---------------------------------------------------------------------
        cls.pylg_enable = settings["pylg_enable"]
        cls.pylg_file = settings["pylg_file"]
        cls.default_exception_warning = settings["default_exception_warning"]
        cls.default_exception_tb_file = settings["default_exception_tb_file"]
        cls.default_exception_tb_stderr = \
            settings["default_exception_tb_stderr"]
        cls.default_exception_exit = settings["default_exception_exit"]
        cls.trace_time = settings["trace_time"]
        cls.time_format = settings["time_format"]
        cls.trace_filename = settings["trace_filename"]
        cls.filename_column_width = settings["filename_column_width"]
        cls.trace_lineno = settings["trace_lineno"]
        cls.lineno_width = settings["lineno_width"]
        cls.trace_function = settings["trace_function"]
        cls.function_column_width = settings["function_column_width"]
        cls.class_name_resolution = settings["class_name_resolution"]
        cls.trace_message = settings["trace_message"]
        cls.message_width = settings["message_width"]
        cls.message_wrap = settings["message_wrap"]
        cls.message_mark_truncation = settings["message_mark_truncation"]
        cls.trace_self = settings["trace_self"]
        cls.collapse_lists = settings["collapse_lists"]
        cls.collapse_dicts = settings["collapse_dicts"]
        cls.default_trace_args = settings["default_trace_args"]
        cls.default_trace_rv = settings["default_trace_rv"]
        cls.default_trace_rv_type = settings["default_trace_rv_type"]

        if not cls.class_name_resolution:
            ClassNameStack.disable()

        cls.wfile = open(cls.pylg_file, "w")
        cls.wfile.write(
            "=== Log initialised at {} ===\n\n".format(datetime.now())
        )

    @classmethod
    def write(cls, string: str):
        """Write to the log file.

        A new log file is opened and initialised if it has not been opened yet.

        Parameters
        ----------
        string : str
            The string to be written to the log file.

        """

        cls.wfile.write(string)
        cls.wfile.flush()

    @classmethod
    def close(cls):
        """Close the log file."""

        if cls.wfile is not None:
            cls.wfile.close()
            cls.wfile = None
        else:
            warnings.warn("PyLg wfile is not open - nothing to close")


# pylint: disable=too-many-instance-attributes
class TraceFunction:
    """Decorator to trace entry and exit from functions.

    Used by appending @TraceFunction on top of the definition of the function
    to trace.

    """

    # pylint: disable=too-few-public-methods
    class TraceFunctionStruct:
        """Internal object to handle traced function properties."""

        function = None
        varnames = None
        defaults = None

        filename = None
        lineno = None
        classname = None
        functionname = None

    def __get__(self, obj, objtype):
        """Support for instance functions."""
        return partial(self.__call__, obj)

    def __init__(self, *args, **kwargs):
        # ---------------------------------------------------------------------
        # Make sure this decorator is never called with no arguments.
        # ---------------------------------------------------------------------
        assert args or kwargs

        if args:

            self._exception_warning = PyLg.default_exception_warning
            self._exception_tb_file = PyLg.default_exception_tb_file
            self._exception_tb_stderr = PyLg.default_exception_tb_stderr
            self._exception_exit = PyLg.default_exception_exit

            self._trace_args = PyLg.default_trace_args
            self._trace_rv = PyLg.default_trace_rv
            self._trace_rv_type = PyLg.default_trace_rv_type

            # -----------------------------------------------------------------
            # The function init_function will verify the input.
            # -----------------------------------------------------------------
            self.init_function(*args, **kwargs)

        if kwargs:

            # -----------------------------------------------------------------
            # If kwargs is non-empty, args should be empty.
            # -----------------------------------------------------------------
            assert not args

            exception_warning_str = 'exception_warning'
            exception_tb_file_str = 'exception_tb_file'
            exception_tb_stderr_str = 'exception_tb_stderr'
            exception_exit_str = 'exception_exit'

            trace_args_str = 'trace_args'
            trace_rv_str = 'trace_rv'
            trace_rv_type_str = 'trace_rv_type'

            kwopts = {}
            for option, default in [
                    (exception_warning_str, PyLg.default_exception_warning),
                    (exception_tb_file_str, PyLg.default_exception_tb_file),
                    (exception_tb_stderr_str,
                     PyLg.default_exception_tb_stderr),
                    (exception_exit_str, PyLg.default_exception_exit),
                    (trace_args_str, PyLg.default_trace_args),
                    (trace_rv_str, PyLg.default_trace_rv),
                    (trace_rv_type_str, PyLg.default_trace_rv_type),
            ]:

                kwopts[option] = kwargs.get(option, default)
                if not _pylg_check_bool(kwopts[option]):
                    raise ValueError(
                        "Invalid type for {} - should be bool, is type {}"
                        .format(option, type(kwopts[option]).__name__)
                    )

            self._exception_warning = kwopts[exception_warning_str]
            self._exception_tb_file = kwopts[exception_tb_file_str]
            self._exception_tb_stderr = kwopts[exception_tb_stderr_str]
            self._exception_exit = kwopts[exception_exit_str]

            self._trace_args = kwopts[trace_args_str]
            self._trace_rv = kwopts[trace_rv_str]
            self._trace_rv_type = kwopts[trace_rv_type_str]

            self.function = None

    def __call__(self, *args, **kwargs):
        """Wrapper that is called when a call to a decorated function is made.

        It also handles extra initialisation when parameters are passed to
        TraceFunction.

        """

        # ---------------------------------------------------------------------
        # __call__ has to behave differently depending on whether the decorator
        # has been given any parameters. The reason for this is as follows:
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
        # In both cases, the result should be a callable object which will be
        # called whenever the decorated function is called. In the first case,
        # the callable object is an instance of TraceFunction, in the latter
        # case the return value of TraceFunction.__call__ is the callable
        # object.
        # ---------------------------------------------------------------------

        if self.function is None:
            # -----------------------------------------------------------------
            # If the decorator has been passed a parameter, __init__ will not
            # define self.function and __call__ will be called immediately
            # after __init__ with the decorated function as the only parameter.
            # Therefore, this __call__ function has to return the callable
            # object that is meant to be called every time the decorated
            # function is called. Here, self is returned in order to return the
            # object as the callable handle for the decorated function. This if
            # block should be hit only once at most and only during
            # initialisation.
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
        except Exception as exc:
            self.trace_exception(exc)

            if self._exception_exit:
                warnings.warn("Exit forced by EXCEPTION_EXIT")

                # pylint: disable=protected-access
                os._exit(1)

            raise

        self.trace_exit(rv)
        ClassNameStack.pop()

        return rv

    def init_function(self, *args, **kwargs):
        """Initialise the TraceFunctionStruct kept by the decorator."""

        # ---------------------------------------------------------------------
        # This function should only ever be called with one parameter - the
        # function to be decorated. These checks are done here, rather than by
        # the caller, as anything that calls this function should also have
        # been called with the decorated function as its only parameter.
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
        # init_function is called from either __init__ or __call__ and we want
        # the frame before that.
        # ---------------------------------------------------------------------
        frames_back = 2
        caller_frame = inspect.stack()[frames_back]

        self.function.filename = os.path.basename(caller_frame[1])
        self.function.lineno = caller_frame[2]
        self.function.classname = caller_frame[3]
        self.function.functionname = self.function.function.__name__

    def trace_entry(self, *args, **kwargs):
        """Handle function entry.

        This function collects all the function arguments and constructs a
        message to pass to trace.

        """

        # ---------------------------------------------------------------------
        # The ENTRY message.
        # ---------------------------------------------------------------------
        msg = "-> ENTRY"
        if args or kwargs:
            msg += ": "

            n_args = len(args)
            if self._trace_args:
                for arg in range(n_args):

                    if not PyLg.trace_self and \
                       self.function.varnames[arg] == "self":
                        continue

                    msg += "{} = {}, ".format(
                        self.function.varnames[arg],
                        self.get_value_string(args[arg])
                    )

                for name in self.function.varnames[n_args:]:
                    msg += "{} = {}, ".format(
                        name, kwargs.get(name, self.function.defaults[name])
                    )

                msg = msg[:-2]

            else:
                msg += "---"

        trace(msg, function=self.function)

    def trace_exit(self, rv=None):
        """Handle function exit.

        Log the fact that a function has finished executing.

        """

        # ---------------------------------------------------------------------
        # The EXIT message.
        # ---------------------------------------------------------------------
        msg = "<- EXIT "
        if rv is not None:
            msg += ": "
            if self._trace_rv:
                msg += self.get_value_string(rv)
            else:
                msg += "---"

            if self._trace_rv_type:
                msg += " (type: {})".format(type(rv).__name__)

        trace(msg, function=self.function)

    def trace_exception(self, exception):
        """Called when a function terminated due to an exception.

        """

        # ---------------------------------------------------------------------
        # The EXIT message.
        # ---------------------------------------------------------------------
        core_msg = type(exception).__name__ + " RAISED"
        msg = "<- EXIT : " + core_msg

        if str(exception) != "":
            msg += " - " + str(exception)

        if self._exception_warning:
            warnings.warn(core_msg, RuntimeWarning)

        if self._exception_tb_file:
            msg += "\n--- EXCEPTION ---\n"
            msg += traceback.format_exc()
            msg += "-----------------"

        if self._exception_tb_stderr:
            print("--- EXCEPTION ---", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
            print("-----------------", file=sys.stderr)

        trace(msg, function=self.function)

    @staticmethod
    def get_value_string(value):
        """Convert value to a string for the log."""

        if isinstance(value, list) and PyLg.collapse_lists:
            return "[ len={} ]".format(len(value))

        if isinstance(value, dict) and PyLg.collapse_dicts:
            return "{{ len={} }}".format(len(value))

        return "{}".format(value)


def trace(message, function=None):
    """Write message to the log file.

    It will also log the time, filename, line number and function name.

    Parameters
    ----------
    message : str
        The log message.
    function : Optional[TraceFunctionStruct]
        A TraceFunctionStruct object if called from within TraceFunction.

    """

    if function is None:
        # ---------------------------------------------------------------------
        # If there is no function object, we need to work out where the trace
        # call was made from.
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
    # If _CLASS_NAME_RESOLUTION is enabled, the top element of the stack should
    # be the class name of the function from which this trace call is made.
    # This cannot be policed so the user must make sure this is the case by
    # ensuring that trace is only called outside of any function or from within
    # functions that have the @TraceFunction decorator.
    # -------------------------------------------------------------------------
    classname = ClassNameStack.get()
    if classname is not None and classname != "<module>":
        functionname = "{}.{}".format(classname, functionname)

    # -------------------------------------------------------------------------
    # Generate the string based on the settings.
    # -------------------------------------------------------------------------
    msg = ""

    if PyLg.trace_time:
        msg += datetime.now().strftime(PyLg.time_format) + "  "

    if PyLg.trace_filename:
        msg += "{filename:{w}.{w}}  ".format(
            filename=filename,
            w=PyLg.filename_column_width
        )

    if PyLg.trace_lineno:
        msg += "{lineno:0{w}}: ".format(lineno=lineno, w=PyLg.lineno_width)

    if PyLg.trace_function:
        msg += "{function:{w}.{w}}  ".format(
            function=functionname,
            w=PyLg.function_column_width
        )

    if PyLg.trace_message:

        message = str(message)

        # ---------------------------------------------------------------------
        # Get the length of the trace line so far
        # ---------------------------------------------------------------------
        premsglen = len(msg)

        # ---------------------------------------------------------------------
        # Split into lines which will be handled separately.
        # ---------------------------------------------------------------------
        lines = message.splitlines()

        if not lines:
            lines = [""]

        for idx, line in enumerate(lines):
            # -----------------------------------------------------------------
            # Wrap the text.
            # -----------------------------------------------------------------
            wrapped = textwrap.wrap(line, PyLg.message_width)

            if not wrapped:
                wrapped = [""]

            # -----------------------------------------------------------------
            # If this is the first line of the whole trace message, it gets
            # special treatment as it doesn't need whitespace in front of it.
            # Otherwise, align it with the previous line.
            # -----------------------------------------------------------------
            if idx != 0:
                msg += "{:{w}}".format("", w=premsglen)

            if PyLg.message_wrap:

                # -------------------------------------------------------------
                # The first wrapped line gets special treatment as any
                # whitespace should already be prepended.
                # -------------------------------------------------------------
                msg += wrapped[0]

                # -------------------------------------------------------------
                # Print the remaining lines. Append whitespace to align it with
                # the first line.
                # -------------------------------------------------------------
                for wrline in wrapped[1:]:
                    msg += "\n{:{w}}".format('', w=premsglen) + wrline

            else:
                # -------------------------------------------------------------
                # The message is not being wrapped.
                # -------------------------------------------------------------

                if PyLg.message_mark_truncation and wrapped[1:]:
                    # ---------------------------------------------------------
                    # We want to mark truncated lines so we need to determine
                    # if the line is being truncated. If it is we replace the
                    # last character with '\'.
                    # ---------------------------------------------------------

                    if PyLg.message_width > 1:
                        wrapped = textwrap.wrap(
                            wrapped[0],
                            PyLg.message_width - 1
                        )
                        assert wrapped

                        msg += "{m:{w}}\\".format(
                            m=wrapped[0],
                            w=PyLg.message_width - 1,
                        )

                    else:
                        assert PyLg.message_width == 1
                        msg += '\\'

                else:
                    # ---------------------------------------------------------
                    # Either the message is not being truncated or
                    # MESSAGE_MARK_TRUNCATION is False.
                    # ---------------------------------------------------------
                    msg += wrapped[0]

            # -----------------------------------------------------------------
            # Terminate with a newline.
            # -----------------------------------------------------------------
            msg += "\n"

    # -------------------------------------------------------------------------
    # Write the data to the log file.
    # -------------------------------------------------------------------------
    PyLg.write(msg)
