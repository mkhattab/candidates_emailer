import os
import sys
import site

PROJECT_DIR = os.path.join(os.path.dirname(__file__), "../project")
site.addsitedir("/home/ubuntu/.virtualenvs/lib/python2.6/site-packages")
sys.path.insert(0, PROJECT_DIR)

from app import app as application
