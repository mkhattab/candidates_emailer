import sys

from flask import Flask
from flask import render_template, session
from flaskext.odesk import odesk

try:
    import odesk_settings
except ImportError:
    raise ImportError("Please create an odesk_settings.py file with secret keys")

app = Flask(__name__)
app.config.from_pyfile("settings.py")
app.register_module(odesk, url_prefix="/odesk")


def init_db():
    import models
    models.db.create_all()


@app.route("/")
def index():
   return render_template("index.html")


@app.route("/is-authorized")
def is_authorized():
    if odesk.is_authorized():
        return "You are authorized!"
    else:
        return "Not authorized!"


@odesk.after_login
def save_session():
    from models import User, db
    from sqlalchemy.exc import IntegrityError

    access_token = odesk.get_access_token()
    u = odesk.get_client().hr.get_user("me")
    user = User(email=u.get("email"),
                first_name=u.get("first_name"),
                last_name=u.get("last_name"),
                access_token=access_token[0],
                access_token_secret=access_token[1])

    session["user"] = {
        "name": "{0}".format(user.full_name),
        "url": u.get("public_url")
        }

    try:
        db.session.add(user)
    except IntegrityError:
        #Update access token
        db.session.rollback()
        user = User.query.get(user.email)
        user.access_token = access_token[0]
        user.access_token_secret = access_token[1]
        db.session.commit()

        
if __name__ == '__main__':
    host = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
    port = None
    if len(host.split(":")) > 1: host, port = host.split(":")

    if "debug" in sys.argv: debug = True
    else: debug = False

    init_db()
    
    app.run(host=host, port=int(port,10) if port else 5000, debug=debug)
