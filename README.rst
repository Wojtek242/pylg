PyLg
====

PyLg (read as py-log) is a python module that facilitates the process
of writing runtime logs. The goal of PyLg is to provide an unobtrusive
and flexible interface that automates the process of generating
informative logs.

Demo
----

.. image:: https://gitlab.wojciechkozlowski.eu/wojtek/PyLg/raw/pylg-dev/screenshots/demo.png
  :target: https://gitlab.wojciechkozlowski.eu/wojtek/PyLg/raw/pylg-dev/screenshots/demo.png

Features
--------

- Ease of use - the API consists of only one decorator and one
  function.
- Flexible - the user can set global preferences as well as on a
  per-function basis.
- Informative - PyLg can automatically log input arguments, return
  values and exceptions raised.
- User logs - the user can make additional logs that will be collected
  together with the automatically generated logs.

Installation
------------

::

   [sudo] pip install pylg --upgrade

Note that PyLg is under active development. Frequent upgrades are
recommended.

Usage
-----

Import the module:

::

   from pylg import TraceFunction, trace

To automatically log function entry and exit use the
``@TraceFunction`` decorator:

::

   @TraceFunction
   def some_fuction():
       pass

Despite the name, this works for both functions and methods.

``@TraceFunction`` can take up to seven optional arguments:

- ``exception_warning`` - if ``True``, PyLg will print a warning about
  every exception caught to ``stderr``.

- ``exception_tb_file`` - if ``True``, PyLg will write the exception
  tracebacks to the log file.

- ``exception_tb_stderr`` - if ``True``, PyLg will print the exception
  tracebacks to ``stderr``.

- ``exception_exit`` - if ``True``, PyLg will force the program to
  exit (and not just raise SystemExit) whenever an exception
  occurs. This will happen even if the exception would be handled at a
  later point.

- ``trace_args`` - if ``True``, PyLg will log input parameters.

- ``trace_rv`` - if ``True``, PyLg will log return values.

- ``trace_rv_type`` - if ``True``, PyLg will log return value types.

The default values for these arguments are set in a global settings
file.

These arguments have to specified explicitly by name. Some examples:

::

   @TraceFunction(trace_args = False)
   def some_fuction():
       pass

   @TraceFunction(trace_args = False, exception_tb_stderr = True)
   def some_fuction():
       pass

The other way to interact with PyLg is to log a user defined message
with the ``trace`` function.

::

   trace("The user can pass any string they desire in here")

User Settings
-------------

The user can adjust several settings to suit their preferences. To do
so, create a file named ``pylg_settings.py`` somewhere in your path
and set any of the following variables to the desired values in order
to override the defaults. The settings.py file in the project
directory contains all the default settings and can be used as a
template.

- ``PYLG_ENABLE`` (default = ``True``) - enable/disable PyLg.

- ``PYLG_FILE`` (default = ``'pylg.log'``) - the log file name.

- ``DEFAULT_EXCEPTION_WARNING`` (default = ``True``) - the default
  setting for ``exception_warning``.

- ``DEFAULT_EXCEPTION_TB_FILE`` (default = ``True``) - the default
  setting for ``exception_tb_file``.

- ``DEFAULT_EXCEPTION_TB_STDERR`` (default = ``False``) - the default
  setting for ``exception_tb_stderr``.

- ``DEAULT_EXCEPTION_EXIT`` (default = ``False``) - the default
  setting for ``exception_exit``.

- ``TRACE_TIME`` (default = ``TRUE``) - enable/disable time logging.

- ``TIME_FORMAT`` (default = ``"%Y-%m-%d %H:%M:%S.%f"``) - formatting
  for the time trace. For a full list of options, see
  https://docs.python.org/2/library/datetime.html#strftime-strptime-behavior.

- ``TRACE_FILENAME`` (default = ``True``) - enable/disable file name
  logging.

- ``FILENAME_COLUMN_WIDTH`` (default = ``20``) - the column width for
  the file name. If a name is too long, it will be truncated.

- ``TRACE_LINENO`` (default = ``True``) - enable/disable the logging
  of the line number from which the trace call was made. For entry and
  exit messages this logs the line in which the decorator is placed
  (which should be directly above the function itself).

- ``LINENO_WIDTH`` (default = ``4``) - the minimum number of digits to
  use to print the line number. If the number is too long, more digits
  will be used.

- ``TRACE_FUNCTION`` (default = ``True``) - enable/disable the logging
  of the function name from which the trace call was made. Entry/exit
  logs refer to the function they enter into and exit from.

- ``FUNCTION_COLUMN_WIDTH`` (default = ``32``) - the column width for
  the function name. If a name is too long, it will be truncated.

- ``CLASS_NAME_RESOLUTION`` (default = ``False``) - enable/disable
  class name resolution. Function names will be printed with their
  class names. IMPORTANT: If this setting is enabled, the trace
  function should ONLY be called from within functions that have the
  ``@TraceFunction`` decorator OR outside of any function.

- ``TRACE_MESSAGE`` (default = ``True``) - enable/disable message
  logging.

- ``MESSAGE_WIDTH`` (default = ``0``) - the column width for the
  message. A width of zero means unlimited.

- ``MESSAGE_WRAP`` (default = ``True``) - if ``True``, PyLg will wrap
  the message to fit within the column width. Otherwise, the message
  will be truncated.

- ``MESSAGE_MARK_TRUNCATION`` (default = ``True``) - if ``True``,
  truncated message lines should have the last character replaced with
  ``\``.

- ``TRACE_SELF`` (default = ``False``) - enable/disable logging of the
  ``self`` function argument.

- ``COLLAPSE_LISTS`` (default = ``False``) - if ``True`` lists will be
  collapsed to ``[ len=x ]`` where ``x`` denotes the number of
  elements in the list.

- ``COLLAPSE_DICTS`` (default = ``False``) - if ``True`` dictionaries
  will be collapsed to ``{ len=x }`` where ``x`` denotes the number of
  elements in the dictionary.

- ``DEFAULT_TRACE_ARGS`` (default = ``True``) - the default setting
  for ``trace_args``.

- ``DEFAULT_TRACE_RV`` (default = ``True``) - the default setting for
  ``trace_rv``.

- ``DEFAULT_TRACE_RV_TYPE`` (default = ``True``) - the default setting
  for ``trace_rv_type``.

Under development
-----------------

Since this module is under development, here are a few things to keep
in mind when using PyLg.

- The behaviour of ``@TraceFunction`` has not been tested when multiple
  decorators are present.
- When PyLg opens a new log file, it overwrites any file present with
  the same name. Therefore, it can erase important files if you are
  not careful.
- Some features of PyLg do not work with old-style classes.

Contributing
------------

Please submit contributions branched from the ``pylg-dev`` branch.
