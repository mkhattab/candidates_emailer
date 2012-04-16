from flask import Flask

app = Flask(__name__)
app.config.from_pyfile("settings.py")

from candidates_emailer import views
from candidates_emailer import models

models.db.app = app
models.db.init_app(app)
models.db.create_all()
