from flaskext.wtf import Form, BooleanField, Required, Email
from flaskext.wtf.html5 import EmailField

class OptionsForm(Form):
    email = EmailField("Email:",
                       validators=[Required(message="Please enter an email address."),
                                   Email(message="Please enter a correct email address.")])
    send_email = BooleanField("Send me emails:",
                              validators=[Required(),])
