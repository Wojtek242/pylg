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

import traceback
import warnings
import inspect
import sys
import os

# -----------------------------------------------------------------------------
# Import all the defaults first.
# -----------------------------------------------------------------------------
from .settings import *

# -----------------------------------------------------------------------------
# The filename of the user settings. It will be set once it can be
# determined after loading the module.
# -----------------------------------------------------------------------------
PYLG_USER_FILE = None

# -----------------------------------------------------------------------------
# Attempt to load the module pylg_settings module. If successful, set
# PYLG_USER_FILE to the module's path. By attempting an import rather
# than checking if a file exists, we can handle the case of the user
# having the settings file elsewhere in their path.
# -----------------------------------------------------------------------------
try:

    # -------------------------------------------------------------------------
    # We import the module itself to be able to determine its source
    # file before we import all the settings.
    # -------------------------------------------------------------------------
    import pylg_settings
    from pylg_settings import *
    PYLG_USER_FILE = inspect.getsourcefile(pylg_settings)

except ImportError:
    # -------------------------------------------------------------------------
    # The user settings don't exist. We assume the user is happy with
    # the defaults.
    # -------------------------------------------------------------------------
    pass

except (NameError, SyntaxError):

    warnings.warn("There was a problem importing user settings")

    sys.stderr.write("\n")
    traceback.print_exc(file=sys.stderr)
    sys.stderr.write("\n")


# -----------------------------------------------------------------------------
# Utility functions for sanity checking user settings. They raise an
# ImportError if something is wrong.
# -----------------------------------------------------------------------------
def pylg_check_bool(value, name):

    if not isinstance(value, bool):

        warning_msg = ("Invalid type for " + name + " in " +
                       PYLG_USER_FILE +
                       " - should be bool, is type " +
                       type(value).__name__)

        warnings.warn(warning_msg)

        raise ImportError


def pylg_check_string(value, name):

    if not isinstance(value, basestring):

        warning_msg = ("Invalid type for " + name + " in " +
                       PYLG_USER_FILE +
                       " - should be a string, is type " +
                       type(value).__name__)

        warnings.warn(warning_msg)

        raise ImportError


def pylg_check_int(value, name):

    # -------------------------------------------------------------------------
    # We check for bool as well as bools are an instance of int, but
    # we don't want to let that go through.
    # -------------------------------------------------------------------------
    if not isinstance(value, int) or isinstance(value, bool):

        warning_msg = ("Invalid type for " + name + " in " +
                       PYLG_USER_FILE +
                       " - should be int, is " +
                       type(value).__name__)

        warnings.warn(warning_msg)

        raise ImportError


def pylg_check_nonneg_int(value, name):

    pylg_check_int(value, name)

    if value < 0:

        warning_msg = ("Invalid value for " + name + " in " +
                       PYLG_USER_FILE +
                       " - should be non-negative, is " +
                       str(value))

        warnings.warn(warning_msg)

        raise ImportError


def pylg_check_pos_int(value, name):

    pylg_check_int(value, name)

    if value <= 0:

        warning_msg = ("Invalid value for " + name + " in " +
                       PYLG_USER_FILE +
                       " - should be positive, is " +
                       str(value))

        warnings.warn(warning_msg)

        raise ImportError


if PYLG_USER_FILE is not None:
    # -------------------------------------------------------------------------
    # If PYLG_USER_FILE is set, we have successfully imported user
    # settings. Nowe, we need to sanity check them. If anything is
    # wrong we reset the value to its default. At this stage a single
    # error should not affect any other settings.
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # PYLG_ENABLE - bool
    # -------------------------------------------------------------------------
    try:
        pylg_check_bool(PYLG_ENABLE, "PYLG_ENABLE")
    except ImportError:
        from .settings import PYLG_ENABLE

    # -------------------------------------------------------------------------
    # PYLG_FILE - string
    # -------------------------------------------------------------------------
    try:
        pylg_check_string(PYLG_FILE, "PYLG_FILE")
    except ImportError:
        from .settings import PYLG_FILE

    # -------------------------------------------------------------------------
    # EXCEPTION_WARNING - bool
    # -------------------------------------------------------------------------
    try:
        pylg_check_bool(EXCEPTION_WARNING, "EXCEPTION_WARNING")
    except ImportError:
        from .settings import EXCEPTION_WARNING

    # -------------------------------------------------------------------------
    # EXCEPTION_EXIT - bool
    # -------------------------------------------------------------------------
    try:
        pylg_check_bool(EXCEPTION_EXIT, "EXCEPTION_EXIT")
    except ImportError:
        from .settings import EXCEPTION_EXIT

    # -------------------------------------------------------------------------
    # TRACE_TIME - bool
    # -------------------------------------------------------------------------
    try:
        pylg_check_bool(TRACE_TIME, "TRACE_TIME")
    except ImportError:
        from .settings import TRACE_TIME

    # -------------------------------------------------------------------------
    # TIME_FORMAT - string
    # -------------------------------------------------------------------------
    try:
        pylg_check_string(TIME_FORMAT, "TIME_FORMAT")
    except ImportError:
        from .settings import TIME_FORMAT

    # -------------------------------------------------------------------------
    # TRACE_FILENAME - bool
    # -------------------------------------------------------------------------
    try:
        pylg_check_bool(TRACE_FILENAME, "TRACE_FILENAME")
    except ImportError:
        from .settings import TRACE_FILENAME

    # -------------------------------------------------------------------------
    # FILENAME_COLUMN_WIDTH - non-negative integer
    # -------------------------------------------------------------------------
    try:
        pylg_check_pos_int(FILENAME_COLUMN_WIDTH, "FILENAME_COLUMN_WIDTH")
    except ImportError:
        from .settings import FILENAME_COLUMN_WIDTH

    # -------------------------------------------------------------------------
    # TRACE_LINENO - bool
    # -------------------------------------------------------------------------
    try:
        pylg_check_bool(TRACE_LINENO, "TRACE_LINENO")
    except ImportError:
        from .settings import TRACE_LINENO

    # -------------------------------------------------------------------------
    # LINENO_WIDTH - non-negative integer
    # -------------------------------------------------------------------------
    try:
        pylg_check_nonneg_int(LINENO_WIDTH, "LINENO_WIDTH")
    except ImportError:
        from .settings import LINENO_WIDTH

    # -------------------------------------------------------------------------
    # TRACE_FUNCTION - bool
    # -------------------------------------------------------------------------
    try:
        pylg_check_bool(TRACE_FUNCTION, "TRACE_FUNCTION")
    except ImportError:
        from .settings import TRACE_FUNCTION

    # -------------------------------------------------------------------------
    # FUNCTION_COLUMN_WIDTH - non-negative integer
    # -------------------------------------------------------------------------
    try:
        pylg_check_pos_int(FUNCTION_COLUMN_WIDTH, "FUNCTION_COLUMN_WIDTH")
    except ImportError:
        from .settings import FUNCTION_COLUMN_WIDTH

    # -------------------------------------------------------------------------
    # CLASS_NAME_RESOLUTION - bool
    # -------------------------------------------------------------------------
    try:
        pylg_check_bool(CLASS_NAME_RESOLUTION, "CLASS_NAME_RESOLUTION")
    except ImportError:
        from .settings import CLASS_NAME_RESOLUTION

    # -------------------------------------------------------------------------
    # TRACE_MESSAGE - bool
    # -------------------------------------------------------------------------
    try:
        pylg_check_bool(TRACE_MESSAGE, "TRACE_MESSAGE")
    except ImportError:
        from .settings import TRACE_MESSAGE

    # -------------------------------------------------------------------------
    # MESSAGE_WIDTH - non-negative integer - note 0 denotes unlimited
    # -------------------------------------------------------------------------
    try:
        pylg_check_nonneg_int(MESSAGE_WIDTH, "MESSAGE_WIDTH")
    except ImportError:
        from .settings import MESSAGE_WIDTH

    # -------------------------------------------------------------------------
    # MESSAGE_WRAP - bool
    # -------------------------------------------------------------------------
    try:
        pylg_check_bool(MESSAGE_WRAP, "MESSAGE_WRAP")
    except ImportError:
        from .settings import MESSAGE_WRAP

    # -------------------------------------------------------------------------
    # MESSAGE_MARK_TRUNCATION - bool
    # -------------------------------------------------------------------------
    try:
        pylg_check_bool(MESSAGE_MARK_TRUNCATION, "MESSAGE_MARK_TRUNCATION")
    except ImportError:
        from .settings import MESSAGE_MARK_TRUNCATION

    # -------------------------------------------------------------------------
    # TRACE_SELF - bool
    # -------------------------------------------------------------------------
    try:
        pylg_check_bool(TRACE_SELF, "TRACE_SELF")
    except ImportError:
        from .settings import TRACE_SELF

    # -------------------------------------------------------------------------
    # COLLAPSE_LISTS - bool
    # -------------------------------------------------------------------------
    try:
        pylg_check_bool(COLLAPSE_LISTS, "COLLAPSE_LISTS")
    except ImportError:
        from .settings import COLLAPSE_LISTS

    # -------------------------------------------------------------------------
    # COLLAPSE_DICTS - bool
    # -------------------------------------------------------------------------
    try:
        pylg_check_bool(COLLAPSE_DICTS, "COLLAPSE_DICTS")
    except ImportError:
        from .settings import COLLAPSE_DICTS

    # -------------------------------------------------------------------------
    # DEFAULT_TRACE_ARGS - bool
    # -------------------------------------------------------------------------
    try:
        pylg_check_bool(DEFAULT_TRACE_ARGS, "DEFAULT_TRACE_ARGS")
    except ImportError:
        from .settings import DEFAULT_TRACE_ARGS

    # -------------------------------------------------------------------------
    # DEFAULT_TRACE_RV - bool
    # -------------------------------------------------------------------------
    try:
        pylg_check_bool(DEFAULT_TRACE_RV, "DEFAULT_TRACE_RV")
    except ImportError:
        from .settings import DEFAULT_TRACE_RV
