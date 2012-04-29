import os
import tempfile
import shutil
from unittest import TestCase
from mock import Mock, patch, MagicMock

import flaskext.testing

from candidates_emailer.reports import *
from test_api import TEST_JOBS, TEST_TEAMS, TEST_OFFERS, TEST_COMPANIES, TEST_ROLES


class ReportsTest(flaskext.testing.TestCase):
    def create_app(self):
        from candidates_emailer import app
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
        app.config["TESTING"] = True
        return app
    
    def setUp(self):
        self.orig_client = odesk.Client
        from candidates_emailer.models import db
        self.db = db
        self.db.create_all()
        self.tmp_reports_dir = tempfile.mkdtemp("reports")
        self.user = User(email="acooper@example.com",
                         first_name="Alice",
                         last_name="Cooper",
                         access_token="__access_token__",
                         access_token_secret="__access_token_secret__")
        self.db.session.add(self.user)
        self.db.session.commit()
        
        client = Mock()
        client.hr.get_companies.return_value = TEST_COMPANIES
        client.hr.get_jobs.return_value = TEST_JOBS
        client.hr.get_teams.return_value = TEST_TEAMS
        client.hr.get_offers.return_value = TEST_OFFERS
        client.hr.get_user_roles.return_value = TEST_ROLES
        
        self.job_poster = JobPoster(self.user, client)
        
    def tearDown(self):
        odesk.Client = self.orig_client
        for report in self.user.reports.all():
            if report.filename:
                os.remove(report.report_file_path)
                os.rmdir(os.path.dirname(report.report_file_path))
        shutil.rmtree(self.tmp_reports_dir, ignore_errors=True)
        
        self.db.session.remove()
        self.db.drop_all()

    def test_get_client(self):
        with patch("odesk.Client") as mock_client:
            _client = get_client(key="12345_public",
                                secret="12345_secret",
                                user=self.user)
        self.assertEquals(_client.oauth_access_token, self.user.access_token)
        self.assertEquals(_client.oauth_access_token_secret, self.user.access_token_secret)

    def test_generate_offers_report(self):
        company = self.job_poster.companies[0]
        job = self.job_poster.jobs(company)[0]
        filename, output = generate_offers_report(self.job_poster, job)
        expected_result = '''provider__id,provider__name,provider__profile_url,provider_team__reference,hourly_charge_rate,hourly_pay_rate,interview_status,candidacy_status,modified_time\r\nbbobberson,Bob Bobberson,https://www.odesk.com/users/~~ciphertext,,55.56,50,waiting_for_provider,rejected,1334712930000\r\n'''

        self.assertEquals(output, expected_result)
        self.assertEquals(filename[-3:], "csv")

    @patch('odesk.Client')
    def test_generate_reports_first_time(self, mock_client):
        mock_client = mock_client()
        mock_client.hr.get_companies.return_value = TEST_COMPANIES
        mock_client.hr.get_jobs.return_value = TEST_JOBS
        mock_client.hr.get_teams.return_value = TEST_TEAMS
        mock_client.hr.get_offers.return_value = TEST_OFFERS
        mock_client.hr.get_user_roles.return_value = TEST_ROLES
        for report in generate_reports(self.tmp_reports_dir):
            self.assertIsInstance(report[1], list)
            self.assertIsInstance(report[1][0], tuple)
    

class ReportLogTest(flaskext.testing.TestCase):    
    def create_app(self):
        from candidates_emailer import app
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
        app.config["TESTING"] = True
        return app
    
    def setUp(self):
        from candidates_emailer.models import db
        self.db = db
        db.create_all()
        self.tmp_reports_dir = tempfile.mkdtemp("reports")
        self.user = User(email="acooper@example.com",
                         first_name="Alice",
                         last_name="Cooper")
        self.report = ReportLog(self.tmp_reports_dir,
                                user_id=self.user.id)
        self.user.reports.append(self.report)
        self.db.session.add(self.user)
        self.db.session.add(self.report)
        self.db.session.commit()

    def tearDown(self):
        for report in self.user.reports.all():
            if report.filename:
                os.remove(report.report_file_path)
                os.rmdir(os.path.dirname(report.report_file_path))
        os.rmdir(self.tmp_reports_dir)        
        self.db.session.remove()
        self.db.drop_all()

    def test_new_report(self):
        with self.report.report_file() as report_file:
            self.report.filename = os.path.basename(report_file.name)
            self.db.session.commit()
            self.assertEquals("{0}/{1}/{2}".format(self.report.reports_dir,
                                        self.report.user_id,
                                        self.report.filename), report_file.name)

    def test_sha1(self):
        self.test_new_report()
        sha1 = self.report._sha1()
        self.assertEquals(len(sha1), 40)
