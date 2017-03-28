import sys
import inspect


def raiseNotDefined():
    print "Method not implemented: %s" % inspect.stack()[1][3]
    sys.exit(1)
