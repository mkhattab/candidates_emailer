from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True)
    alternate_email = db.Column(db.String)
    use_alternate_email = db.Column(db.Boolean, nullable=False)
    send_email = db.Column(db.Boolean, nullable=False)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    access_token = db.Column(db.String)
    access_token_secret = db.Column(db.String)

    def __init__(self, *args, **kwargs):
        self.email = kwargs.get("email")
        self.first_name = kwargs.get("first_name")
        self.last_name = kwargs.get("last_name")
        self.access_token = kwargs.get("access_token")
        self.access_token_secret = kwargs.get("access_token_secret")
        self.alternate_email = kwargs.get("alternate_email")
        self.use_alternate_email = kwargs.get("use_alternate_email")
        self.send_email = kwargs.get("send_email")
        
        if not self.use_alternate_email:
            self.use_alternate_email = False

        if not self.send_email:
            self.send_email = True

    def __repr__(self):
        return "<User {0}>".format(self.email)

    @property
    def full_name(self):
        return "{0} {1}".format(self.first_name, self.last_name)
