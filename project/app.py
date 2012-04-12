import sys

from flask import Flask
from flask import render_template
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


@app.route("/authorize-test")
def authorize():
    if odesk.is_authorized():
        return "You are authorized!"
    else:
        return "Not authorized!"


if __name__ == '__main__':
    host = sys.argv[1]
    port = None
    if len(host.split(":")) > 1: host, port = host.split(":")

    if "debug" in sys.argv: debug = True
    else: debug = False
    
    app.run(host=host, port=int(port,10) if port else 5000, debug=debug)
