"""Handlers for PyLg settings."""

from typing import Optional

import os
import yaml

_USER_FILE_NAME = "pylg_settings.yml"
_PYLG_FILE_NAME = "settings.yml"

_BOOL_OPTIONS = set([
    "pylg_enable",
    "default_exception_warning",
    "default_exception_tb_file",
    "default_exception_tb_stderr",
    "default_exception_exit",
    "trace_time",
    "trace_filename",
    "trace_lineno",
    "trace_function",
    "class_name_resolution",
    "trace_message",
    "message_wrap",
    "message_mark_truncation",
    "trace_self",
    "collapse_lists",
    "collapse_dicts",
    "default_trace_args",
    "default_trace_rv",
    "default_trace_rv_type",
])

_STRING_OPTIONS = set([
    "pylg_file",
    "time_format",
])

_POS_INT_OPTIONS = set([
    "filename_column_width",
    "function_column_width",
])

_NONNEG_OPTIONS = set([
    "lineno_width",
    "message_width",
])


def load(user_settings_path: Optional[str] = None) -> dict:
    """Load PyLg settings from file.

    If a user provides a settings file, it will be used. Otherwise, PyLg's
    default settings will be read in.

    """

    # -------------------------------------------------------------------------
    # Load the default settings.
    # -------------------------------------------------------------------------

    default_settings_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), _PYLG_FILE_NAME
    )

    with open(default_settings_path, 'r') as settings_file:
        default_settings = yaml.full_load(settings_file)

    # -------------------------------------------------------------------------
    # Load the user settings.
    # -------------------------------------------------------------------------

    user_settings = {}
    if user_settings_path is not None:
        with open(user_settings_path, 'r') as settings_file:
            user_settings = yaml.full_load(settings_file)

    # -------------------------------------------------------------------------
    # Merge the two settings preferring user values over defaults.
    # -------------------------------------------------------------------------

    settings = {**default_settings, **user_settings}

    # -------------------------------------------------------------------------
    # Verify the input.
    # -------------------------------------------------------------------------

    for option in settings.keys():
        source_file = (user_settings_path
                       if option in user_settings
                       else default_settings_path)
        option_type = type(settings[option]).__name__
        option_value = settings[option]

        if option in _BOOL_OPTIONS:
            if not _pylg_check_bool(option_value):
                raise ImportError(
                    "Invalid type for {} in {} - should be bool, is type {}"
                    .format(option, source_file, option_type)
                )

        elif option in _STRING_OPTIONS:
            if not _pylg_check_string(option_value):
                raise ImportError(
                    "Invalid type for {} in {} - should be str, is type {}"
                    .format(option, source_file, option_type)
                )

        elif option in _POS_INT_OPTIONS:
            if not _pylg_check_pos_int(option_value):
                raise ImportError(
                    "Invalid type/value for {} in {} - "
                    "should be positive int, is {}"
                    .format(option, source_file, option_value)
                )

        elif option in _NONNEG_OPTIONS:
            if not _pylg_check_nonneg_int(option_value):
                raise ImportError(
                    "Invalid type/value for {} in {} - "
                    "should be non-negative int, is {}"
                    .format(option, source_file, option_value)
                )

        else:
            raise ImportError("Unrecognised option in {}: {}"
                              .format(source_file, option))

    # -------------------------------------------------------------------------
    # Some final value processing.
    # -------------------------------------------------------------------------
    if settings["message_width"] == 0:
        settings["message_width"] = float("inf")

    return settings


# -----------------------------------------------------------------------------
# Utility functions for sanity checking user settings.
# -----------------------------------------------------------------------------
def _pylg_check_bool(value) -> bool:
    return isinstance(value, bool)


def _pylg_check_string(value) -> bool:
    return isinstance(value, str)


def _pylg_check_int(value) -> bool:

    # -------------------------------------------------------------------------
    # We check for bool as well as bools are an instance of int, but we don't
    # want to let that go through.
    # -------------------------------------------------------------------------
    return isinstance(value, int) and not isinstance(value, bool)


def _pylg_check_nonneg_int(value):
    return _pylg_check_int(value) and value >= 0


def _pylg_check_pos_int(value):
    return _pylg_check_int(value) and value > 0
