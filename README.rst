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

``@TraceFunction`` can take up to two optional arguments:
- trace_args - if ``True``, input parameters will be logged.
- trace_rv   - if ``True``, the return value will be logged.

The default values for these arguments are set in a global settings
file.

These arguments have to specified explicitly by name. Some examples:

::

   @TraceFunction(trace_args = False)
   def some_fuction():
       pass

   @TraceFunction(trace_rv = False)
   def some_fuction():
       pass

   @TraceFunction(trace_args = False, trace_args = False)
   def some_fuction():
       pass

The other way to interact with PyLg is to log a user defined message
with the ``trace`` function.

::

   trace("The user can pass any string they desire in here")

User Settings
-------------

The user can adjust several settings to suit their preferences. To do
so, create a file named ``pylg_settings.py`` in the top-level
directory and set any of the following variables to the desired values
in order to override the defaults. The settings.py file in the project
directory contains all the default settings and can be used as a
template.

- PYLG_ENABLE (default = True) - enable/disable logs.
- PYLG (default = 'pylg.log') - the log file name.
- CLASS_NAME_RESOLUTION (default = False) - PyLg can also log the
  class name along with the method name if one exists. However, for
  this to work correctly the ``trace`` function cannot be called from
  functions that are not decorated by ``@TraceFunction`` which is why
  it is disabled by default.
- DEFAULT_TRACE_ARGS (default = True) - the default value for
  ``trace_args`` argument which can be passed to the ``@TraceFunction`
  decorator. If ``trace_args`` is ``True`` all parameters passed to
  the function will be logged. This can be overriden on an individual
  function basis.
- DEFAULT_TRACE_RV (default = True) - the default value for trace_rv
  argument which can be passed to the ``@TraceFunction`` decorator. If
  ``trace_rv`` is ``True`` the function's return value will be
  logged. This can be overriden on an individual function basis.
- EXCEPTION_WARNING (default = True) - PyLg catches all exceptions in
  traced functions, logs them, and then re-raises them with the full
  backtrace. This setting determines whether it should also produce a
  warning for the user using the Python warning mechanism.
- FILENAME_COLUMN_WIDTH (default = 32) - the column width reserved for
  the file name. Names that are too short will be padded with
  whitespace and names that are too long will be truncated.
- FUNCTION_COLUMN_WIDTH (default = 32) - the column width reserved for
  the function name. Names that are too short will be padded with
  whitespace and names that are too long will be truncated.

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
