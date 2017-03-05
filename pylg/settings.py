#-------------------------------------------------------------------------------
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
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# Enable/disable PyLg.
#-------------------------------------------------------------------------------
PYLG_ENABLE = True

#-------------------------------------------------------------------------------
# Log file.
#-------------------------------------------------------------------------------
PYLG = 'pylg.log'

#-------------------------------------------------------------------------------
# Enable class name resolution. Function names will be printed with
# their class names.
#
# IMPORTANT: If this setting is enabled, the trace function should
# ONLY be called from within functions that have the @TraceFunction
# decorator OR outside of any function.
#-------------------------------------------------------------------------------
CLASS_NAME_RESOLUTION = False

#-------------------------------------------------------------------------------
# The default for whether TraceFunction should trace function
# parameters and return values.
#-------------------------------------------------------------------------------
DEFAULT_TRACE_ARGS = True
DEFAULT_TRACE_RV   = True

#-------------------------------------------------------------------------------
# Whether to warn the user when an Exception has been raised in a
# traced funcion.
#-------------------------------------------------------------------------------
EXCEPTION_WARNING = True

#-------------------------------------------------------------------------------
# The column width for file and function names.
#-------------------------------------------------------------------------------
FILENAME_COLUMN_WIDTH = 32
FUNCTION_COLUMN_WIDTH = 32
