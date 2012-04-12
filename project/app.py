import sys

from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def index():
   return render_template("index.html")


if __name__ == '__main__':
    host = sys.argv[1]
    port = None
    if len(host.split(":")) > 1: host, port = host.split(":")

    if "debug" in sys.argv: debug = True
    else: debug = False
    
    app.run(host=host, port=int(port,10) if port else 5000, debug=debug)
