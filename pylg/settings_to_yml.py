"""Convert old-style settings.py to new-style settings.yml."""

import warnings
import sys
from os import path


def convert(source, destination):
    """Convert source python settings file to destination yml file.

    Parameters
    ----------
    source : str
        File name of the old-style Python settings file.
    destination: str
        File name for the new-style YAML settings file.

    """
    with open(source, 'r') as src, open(destination, 'w') as dst:
        for line in src:
            if not line.lstrip().startswith('#') and '=' in line:
                key, val = line.split('=')
                key = key.strip().lower()
                val = val.strip()
                dst.write("{}: {}\n".format(key, val))
            else:
                dst.write(line)


def settings_to_yml():
    """Convert user settings file from old-style python to new-style YAML."""

    settings_py = "pylg_settings.py"

    root_dir = path.dirname(sys.modules['__main__'].__file__)
    settings_py_path = path.join(root_dir, settings_py)
    if path.isfile(settings_py_path):
        warnings.warn(
            "Deprecated {} found".format(settings_py),
            DeprecationWarning,
        )

        settings_yml = "{}.yml".format(settings_py[:-3])
        settings_yml_path = path.join(root_dir, settings_yml)
        if path.isfile(settings_yml_path):
            warnings.warn(
                "Could not convert {py} to {yml}, {yml} already exists. "
                "If this is the converted settings file, delete {py} to get "
                "rid of this warning."
                .format(py=settings_py, yml=settings_yml),
                DeprecationWarning,
            )
            return

        warnings.warn(
            "Converting {} to {}".format(settings_py, settings_yml),
            DeprecationWarning,
        )
        convert(settings_py_path, settings_yml_path)


if __name__ == "__main__":  # pragma: no cover
    settings_to_yml()
