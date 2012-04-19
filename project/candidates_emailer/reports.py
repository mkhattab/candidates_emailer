import csv
import time
import StringIO
from datetime import datetime
import simplejson as json

import odesk

from candidates_emailer.models import User, ReportLog, db
from candidates_emailer.odesk_settings import ODESK_KEY, ODESK_SECRET
from candidates_emailer.api import *

OFFERS_REPORT_COLUMNS = (
    "provider__id",
    "provider__name",
    "provider__profile_url",
    "provider_team__reference",
    "hourly_charge_rate",
    "hourly_pay_rate",
    "interview_status",
    "candidacy_status",
    "modified_time",
)

def get_client(key=ODESK_KEY, secret=ODESK_SECRET,
               user=None, oauth_access_token=None, oauth_access_token_secret=None):
    if user:
        oauth_access_token = user.access_token
        oauth_access_token_secret = user.access_token_secret

    client = odesk.Client(key, secret, auth="oauth")
    client.oauth_access_token = oauth_access_token
    client.oauth_access_token_secret = oauth_access_token_secret
    
    return client


def generate_offers_report(job_poster, job):
    output = StringIO.StringIO()
    writer = csv.writer(output)
    writer.writerow(OFFERS_REPORT_COLUMNS)
    writer.writerows([[offer.__getattr__(col)
                       for col in OFFERS_REPORT_COLUMNS]
                     for offer in job_poster.offers(job)])
    filename = "{0}_{1}.csv".format("OffersReport",
                                        job.reference)
    return (filename, output.getvalue())


def generate_reports(reports_dir):
    for user in User.query.all():
        last_report = user.reports.order_by(db.desc(ReportLog.timestamp)).first()
        csv_reports = []
        job_poster = JobPoster(user, get_client(user=user))

        for company in job_poster.companies:
            for job in job_poster.jobs(company):
                csv_reports.append(generate_offers_report(job_poster, job))

        report = ReportLog(reports_dir)
        user.reports.append(report)
        db.session.commit()
        
        if not last_report:
            with report.report_file() as report_file:
                report_file.write(json.dumps(csv_reports))
                
            db.session.commit()
            yield csv_reports
        else:
            delta = report.timestamp - last_report.timestamp
            report_sha1 = report._sha1()
            #If time since last report is greater than 12 hours and not a duplicate, continue
            if delta.seconds > 12 * 60 * 60 and \
                   report_sha1 != last_report.sha1:
                report.sha1 = report_sha1
                db.session.commit()
                yield csv_reports
            else:
                report.delete_report_file()
                db.session.delete(report)
                db.session.commit()
