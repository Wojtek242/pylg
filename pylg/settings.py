# -----------------------------------------------------------------------------
# PyLg: module to facilitate and automate the process of writing runtime logs.
# Copyright (C) 2017 Wojciech Kozlowski <wk@wojciechkozlowski.eu>
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

# -----------------------------------------------------------------------------
# Enable/disable PyLg.
# -----------------------------------------------------------------------------
PYLG_ENABLE = True

# -----------------------------------------------------------------------------
# The log file name.
# -----------------------------------------------------------------------------
PYLG_FILE = 'pylg.log'

# -----------------------------------------------------------------------------
# The default value for 'exception_warning'. If True, PyLg will print
# a warning about every exception caught to stderr.
# -----------------------------------------------------------------------------
DEFAULT_EXCEPTION_WARNING = True

# -----------------------------------------------------------------------------
# The default value for 'exception_tb_file'. If True, PyLg will write
# the exception tracebacks to the log file.
# -----------------------------------------------------------------------------
DEFAULT_EXCEPTION_TB_FILE = True

# -----------------------------------------------------------------------------
# The default value for 'exception_tb_file'. If True, PyLg will print
# the exception tracebacks to stderr.
# -----------------------------------------------------------------------------
DEFAULT_EXCEPTION_TB_STDERR = False

# -----------------------------------------------------------------------------
# The default value for 'exception_exit'. If True, PyLg will force the
# program to exit (and not just raise SystemExit) whenever an
# exception occurs. This will happen even if the exception would be
# handled at a later point.
# -----------------------------------------------------------------------------
DEFAULT_EXCEPTION_EXIT = False

# -----------------------------------------------------------------------------
# Enable/disable time logging.
# -----------------------------------------------------------------------------
TRACE_TIME = True

# -----------------------------------------------------------------------------
# Formatting for the time trace. For a full list of options, see
# https://docs.python.org/2/library/datetime.html#strftime-strptime-behavior.
# -----------------------------------------------------------------------------
TIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"

# -----------------------------------------------------------------------------
# Enable/disable file name logging.
# -----------------------------------------------------------------------------
TRACE_FILENAME = True

# -----------------------------------------------------------------------------
# The column width for the file name. If a name is too long, it will
# be truncated.
# -----------------------------------------------------------------------------
FILENAME_COLUMN_WIDTH = 20

# -----------------------------------------------------------------------------
# Enable/disable the logging of the line number from which the trace
# call was made. For entry and exit messages this logs the line in
# which the decorator is placed (which should be directly above the
# function itself).
# -----------------------------------------------------------------------------
TRACE_LINENO = True

# -----------------------------------------------------------------------------
# The minimum number of digits to use to print the line number. If the
# number is too long, more digits will be used.
# -----------------------------------------------------------------------------
LINENO_WIDTH = 4

# -----------------------------------------------------------------------------
# Enable/disable the logging of the function name from which the trace
# call was made. Entry/exit logs refer to the function they enter into
# and exit from.
# -----------------------------------------------------------------------------
TRACE_FUNCTION = True

# -----------------------------------------------------------------------------
# The column width for the function name. If a name is too long, it
# will be truncated.
# -----------------------------------------------------------------------------
FUNCTION_COLUMN_WIDTH = 32

# -----------------------------------------------------------------------------
# Enable/disable class name resolution. Function names will be printed
# with their class names.
#
# IMPORTANT: If this setting is enabled, the trace function should
# ONLY be called from within functions that have the @TraceFunction
# decorator OR outside of any function.
# -----------------------------------------------------------------------------
CLASS_NAME_RESOLUTION = False

# -----------------------------------------------------------------------------
# Enable/disable message logging.
# -----------------------------------------------------------------------------
TRACE_MESSAGE = True

# -----------------------------------------------------------------------------
# The column width for the message. A width of zero means unlimited.
# -----------------------------------------------------------------------------
MESSAGE_WIDTH = 0

# -----------------------------------------------------------------------------
# If True, PyLg will wrap the message to fit within the column
# width. Otherwise, the message will be truncated.
# -----------------------------------------------------------------------------
MESSAGE_WRAP = True

# -----------------------------------------------------------------------------
# If true, truncated message lines should have the last character
# replaced with '\'. Note that this reduces MESSAGE_WIDTH by 1 for
# truncated lines which may truncate words that would've otherwise
# appeared in the message.
# -----------------------------------------------------------------------------
MESSAGE_MARK_TRUNCATION = True

# -----------------------------------------------------------------------------
# Enable/disable logging of the 'self' function argument.
# -----------------------------------------------------------------------------
TRACE_SELF = False

# -----------------------------------------------------------------------------
# If True lists/dictionaries will be collapsed to '[ len=x ]' and '{
# len=x }' respectively, where x denotes the number of elements in the
# collection.
# -----------------------------------------------------------------------------
COLLAPSE_LISTS = False
COLLAPSE_DICTS = False

# -----------------------------------------------------------------------------
# The default setting for 'trace_args'. If True, PyLg will log input
# parameters.
# -----------------------------------------------------------------------------
DEFAULT_TRACE_ARGS = True

# -----------------------------------------------------------------------------
# The default setting for 'trace_rv'. If True, PyLg will log return
# values.
# -----------------------------------------------------------------------------
DEFAULT_TRACE_RV = True

# -----------------------------------------------------------------------------
# The default settings for 'trace_rv_type'. If True, PyLg will log
# return value types.
# -----------------------------------------------------------------------------
DEFAULT_TRACE_RV_TYPE = False
