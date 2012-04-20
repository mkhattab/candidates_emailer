import os
import sys

from flask import Flask 
from flaskext.testing import TestCase

class SiteTest(TestCase):
    def create_app(self):
        from candidates_emailer import app
        app.config["TESTING"] = True
        return app

    def test_index_ok(self):
        response = self.client.get("/")
        self.assertEquals(response.status_code, 200)

    def test_user_does_not_exist(self):
        #TODO
        pass
