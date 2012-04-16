#Project settings
import os

PROJECT_DIR = os.path.dirname(__file__)
def _project_path(*dirs):
    return os.path.join(PROJECT_DIR, *dirs)

SQLALCHEMY_DATABASE_URI = "sqlite:///{0}".format(_project_path("dev.db"))

from candidates_emailer.odesk_settings import *
