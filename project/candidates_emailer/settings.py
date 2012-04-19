#Project settings
import os
import sys

SQLALCHEMY_DATABASE_URI = "sqlite:///dev.db"

from candidates_emailer.odesk_settings import *

try:
    from candidates_emailer.local_settings import *
except ImportError:
    print >> sys.stderr, "No local_settings.py found!"
