import sys

from candidates_emailer import app


if __name__ == '__main__':
    host = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
    port = None
    if len(host.split(":")) > 1: host, port = host.split(":")

    if "debug" in sys.argv: debug = True
    else: debug = False
    
    app.run(host=host, port=int(port,10) if port else 5000, debug=debug)
