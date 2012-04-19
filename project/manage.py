#!/usr/bin/env python
from jinja2 import Template
from flaskext.script import Manager, Command, Option
from flaskext.mail import Mail, Message

from candidates_emailer import app
from candidates_emailer.reports import generate_reports

manager = Manager(app)

class SendReports(Command):
    option_list = (
        Option("--testing", "-t",
               help="just print to stdout instead of sending",
               action="store_true",
               dest="testing"),
        )
    
    def run(self, testing):
        mail = Mail(app)
        for user, csv_report in generate_reports(app.config["REPORTS_DIR"]):
            context = {"user": user}
            template = Template(app.config["EMAIL_TEXT_TEMPLATE"])
            msg = Message(app.config["EMAIL_SUBJECT_LINE"],
                          recipients=[user.alternate_email] if user.use_alternate_email else [user.email],
                          sender=app.config["DEFAULT_MAIL_SENDER"])
            msg.body = template.render(context)

            if not testing:
                mail.send(msg)
            else:
                print msg.get_response().to_message().as_string()

manager.add_command("send_reports", SendReports())

if __name__ == '__main__':
    manager.run()
