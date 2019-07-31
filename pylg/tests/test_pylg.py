from pylg import TraceFunction, trace
import sys

def test_load():
    print(sys.modules['__main__'].__file__)
