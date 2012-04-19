import csv
import time
import StringIO
from datetime import datetime

import odesk

from candidates_emailer.models import User, ReportLog
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
    filename = "{0}_{1}_{2}.csv".format("OffersReport",
                                        job.reference,
                                        int(time.mktime(datetime.now().timetuple()))
                                        )
    return (filename, output)


def generate_reports(template="email.html"):
    pass
