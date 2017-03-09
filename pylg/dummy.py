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

from functools import partial


class TraceFunction(object):

    """ Dummy implementation of TraceFunction.
    """

    def __get__(self, obj, objtype):

        """ Support for instance functions.
        """

        return partial(self.__call__, obj)

    def __init__(self, *args, **kwargs):

        """ Constructor for dummy TraceFunction. Note that the behaviour is
            different depending on whether TraceFunction is passed any
            parameters. For details see the non-dummy implementation.
        """

        # ---------------------------------------------------------------------
        # Make sure this decorator is never called with no arguments.
        # ---------------------------------------------------------------------
        assert args or kwargs

        if args:

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

            self.function = None

    def __call__(self, *args, **kwargs):

        """ The actual wrapper that is called when a call to a
            decorated function is made. It also handles extra
            initialisation when parameters are passed to
            TraceFunction.

            :return: The return value of the decorated function.
        """

        if self.function is None:
            # -----------------------------------------------------------------
            # For an explanation of the logic here, see the non-dummy
            # implementations in pylg.py.
            # -----------------------------------------------------------------
            self.init_function(*args, **kwargs)
            return self

        # ---------------------------------------------------------------------
        # The actual decorating. The dummy implementation doesn't do anything.
        # ---------------------------------------------------------------------
        return self.function(*args, **kwargs)

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

        self.function = args[0]


def trace(message, function=None):
    pass
