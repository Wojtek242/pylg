Changelog
=========

1.3.0
-----

- Added option to trace return value type.
- Added options for tracing exception tracebacks.
- Made all exception options possible to set individually for functions.
- Added support for multi-line trace messages.

1.2.2
-----

- Modified message wrapping code.

1.2.1
-----

- Dummy implementation used when PyLg is disabled has been simplified.

1.2.0
-----

- Fixed bug that didn't preserve exception backtrace correctly.

- Function ``trace`` now automatically converts a message to a string.

- Added several new options that can now be set in
  ``pylg_settings.py``, see the README for details.

- Improved dummy implementation for the case when PyLg is disabled.

- User settings provided in ``pylg_settings.py`` are now checked for
  errors. In the case of a failed import, PyLg will set all settings
  to defaults. In case of an invalid individual value, only the
  relevant setting will be reset to its default.

1.1.0
-----

- PyLg can now be installed with pip.

1.0.0
-----

- Initial PyLg version.
