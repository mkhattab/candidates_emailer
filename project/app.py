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
    u = odesk.get_client().hr.get_user("me")
    session["user"] = {
        "name": "{0} {1}".format(u.get("first_name"), u.get("last_name")),
        "url": u.get("public_url")
        }


if __name__ == '__main__':
    host = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
    port = None
    if len(host.split(":")) > 1: host, port = host.split(":")

    if "debug" in sys.argv: debug = True
    else: debug = False
    
    app.run(host=host, port=int(port,10) if port else 5000, debug=debug)
