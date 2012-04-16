import sys

from sqlalchemy.exc import IntegrityError
from flask import Flask
from flask import render_template,\
     session, request, redirect, url_for
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
init_db()

@app.route("/")
def index():
    if odesk.is_authorized():
        return redirect(url_for("options"))
    else:
        return render_template("index.html")


@app.route("/options/", methods=("GET", "POST"))
@odesk.login_required
def options():
    from forms import OptionsForm
    from models import User, db

    
    user = User.query.get(session["user_id"])
    form = OptionsForm()
    if request.method == "POST" \
           and form.validate():
        user.alternate_email = form.email.data
        user.send_email = form.send_email.data
        user.use_alternate_email = True if user.email != user.alternate_email else False
        db.session.commit()

    if request.method == "GET":
        form = OptionsForm(email=user.alternate_email \
                           if user.use_alternate_email else user.email,
                           send_email=user.send_email)

    
    return render_template("options.html", form=form)


@odesk.after_login
def save_session():
    from models import User, db

    access_token = odesk.get_access_token()
    u = odesk.get_client().hr.get_user("me")
    user = User(email=u.get("email"),
                first_name=u.get("first_name"),
                last_name=u.get("last_name"),
                access_token=access_token[0],
                access_token_secret=access_token[1])

    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        #Update access token
        db.session.rollback()
        user = User.query.filter_by(email=user.email).first()
        user.access_token = access_token[0]
        user.access_token_secret = access_token[1]
        db.session.commit()

    session["user_id"] = user.id
    session["user"] = {
        "name": "{0}".format(user.full_name),
        "url": u.get("public_url")
        }

    
    

        
if __name__ == '__main__':
    host = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
    port = None
    if len(host.split(":")) > 1: host, port = host.split(":")

    if "debug" in sys.argv: debug = True
    else: debug = False

    init_db()
    
    app.run(host=host, port=int(port,10) if port else 5000, debug=debug)
