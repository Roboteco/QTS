import sys

import os

INTERP = os.path.expanduser("/var/www/u1968957/data/flasken/bin/python")
if sys.executable != INTERP:
   os.execl(INTERP, INTERP, *sys.argv)

sys.path.append(os.getcwd())

from application import application