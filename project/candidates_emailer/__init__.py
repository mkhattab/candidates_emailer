from flask import Flask

from candidates_emailer import settings

app = Flask(__name__)
app.config.from_object(settings)

from candidates_emailer import views
from candidates_emailer import models

models.db.app = app
models.db.init_app(app)
models.db.create_all()
