from pylg import TraceFunction, trace, PyLg
import sys

def test_load():

    PyLg.configure(user_settings_path="tests/custom.yml")

    @TraceFunction
    def decorated_function():
        pass

    decorated_function()
