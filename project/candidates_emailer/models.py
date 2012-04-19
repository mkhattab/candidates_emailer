import os
import hashlib
from datetime import datetime

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
    reports = db.relationship('ReportLog', backref="user", lazy="dynamic")

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


class ReportLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    timestamp = db.Column(db.DateTime, nullable=False)
    sha1 = db.Column(db.String)
    filename = db.Column(db.String)


    def __init__(self, reports_dir, *args, **kwargs):
            self.id = kwargs.get("id")
            self.user_id = kwargs.get("user_id")
            self.timestamp = kwargs.get("timestamp")
            self.sha1 = kwargs.get("sha1")
            self.filename = kwargs.get("filename")

            if not self.timestamp:
                self.timestamp = datetime.utcnow()

            self.reports_dir = reports_dir

    def __repr__(self):
        return "<ReportLog ID:{0} File:'{1}'>".format(self.id, self.filename)
    
    def _sha1(self):
        filename = self.report_file_path
        with open(filename, "rb") as f:
            return hashlib.sha1(f.read()).hexdigest()

    def report_file(self):
        if self.filename:
            return open(os.path.join(self.reports_dir,
                                     self.user_id,
                                     self.filename), "rb")
        if not self.user_id:
            raise Exception("This object needs to be attached to a user before creating a report")
        
        try:
            path = os.path.join(self.reports_dir, str(self.user_id))
            os.makedirs(path)
        except os.error as e:
            if e.errno != 17:
                raise e

        if not self.id: raise Exception("You need to save this object before requesting a report file")

        return open(os.path.join(path, "{0}-{1}.rep".format(self.id, self.timestamp)), "wb")

    @property
    def report_file_path(self):
        if self.filename:
            return os.path.join(self.reports_dir, str(self.user_id), self.filename)

    def delete_report_file(self):
        if self.filename:
            try:
                os.remove(self.report_file_path)
            except os.error as e:
                if e.errno != 2:
                    raise e
