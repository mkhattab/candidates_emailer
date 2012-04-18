from unittest import TestCase
from mock import Mock

from candidates_emailer import api


### Test Data ###
TEST_COMPANIES = [{u'name': u'Alice Cooper',
                   u'owner_user_id': u'acooper',
                   u'reference': u'123456',
                   u'status': u'active'}]

TEST_JOBS = {u'job': {u'attachment_file_url': u'',
                      u'budget': u'',
                      u'buyer_company__name': u'Alice Cooper',
                      u'buyer_company__reference': u'123456',
                      u'buyer_team__id': u'6yiq_pfanlnwclja9-smag',
                      u'buyer_team__name': u'Alice Cooper',
                      u'buyer_team__reference': u'123456',
                      u'cancelled_date': u'1334620800000',
                      u'category': u'Web Development',
                      u'count_new_applicants': u'0',
                      u'count_total_applicants': u'0',
                      u'count_total_candidates': u'0',
                      u'created_by': u'acooper',
                      u'created_by_name': u'Alice Cooper',
                      u'created_time': u'1334668229000',
                      u'description': u'This is a test job.',
                      u'duration': u'364',
                      u'end_date': u'1334620800000',
                      u'filled_date': u'',
                      u'job_type': u'hourly',
                      u'last_candidacy_access_time': u'',
                      u'num_active_candidates': u'0',
                      u'num_candidates': u'1',
                      u'num_new_candidates': u'0',
                      u'off_the_network': u'',
                      u'public_url': u'https://www.odesk.com/jobs/~~8b1b0b02acaeba75',
                      u'reference': u'1234567',
                      u'start_date': u'1334620800000',
                      u'status': u'cancelled',
                      u'subcategory': u'Web Programming',
                      u'title': u'Test Job',
                      u'visibility': u'invite-only'},
             u'lister': {u'paging': {u'count': u'20', u'offset': u'0'},
                         u'query': u'',
                         u'sort': {u'sort': {u'sort': [u'created_time', u'asc']}},
                         u'total_items': u'1'}}

TEST_TEAMS = [{u'company__reference': u'123456',
               u'company_name': u'Alice Cooper',
               u'id': u'6yiq_pfanlnwclja9-smag',
               u'is_hidden': u'',
               u'name': u'Alice Cooper',
               u'parent_team__id': u'6yiq_pfanlnwclja9-smag',
               u'parent_team__name': u'Alice Cooper',
               u'parent_team__reference': u'123456',
               u'reference': u'123456',
               u'status': u'active'}]
        

class BaseAPIObjectTest(TestCase):
    def setUp(self):
        self.object = api.BaseAPIObject({"num_int_value": "1",
                                         "num_value_hours": "1.2",
                                         "is_truth_value": "1",
                                         "is_false_value": "",
                                         "string_value": "some value"})

    def test_get_string_field(self):
        assert self.object.string_value == "some value"

    def test_get_boolean_field_true(self):
        assert self.object.is_truth_value == True

    def test_get_boolean_field_false(self):
        assert self.object.is_false_value == False

    def test_get_num_int_field(self):
        assert isinstance(self.object.num_int_value, int) == True

    def test_get_num_float_field(self):
        assert isinstance(self.object.num_value_hours, float) == True


class DummyObject(api.BaseAPIObject):
    type = "objects"
    def __init__(self, _json_cache=None):
        super(DummyObject, self).__init__(_json_cache)


class BaseListTest(TestCase):
    def setUp(self):
        json_data_dict_many = {
            "lister": {
                "paging": {
                    "count": "20",
                    "offset": "0"
                    },
                "query": "",
                "sort": "",
                "total_items": "1"
            }, "objects": [
                {"value": "test"}
                ]}
        self.many_objects_dict = api.BaseList(Mock(),
                                              DummyObject,
                                              _json_cache=json_data_dict_many)
        
        json_data_dict_one = {
            "lister": {
                "paging": {
                    "count": "1",
                    "offset": "0"
                    },
                "query": "",
                "sort": "",
                "total_items": "1"
            }, "objects": {
                "value": "test"
                }}
        self.one_object_dict = api.BaseList(Mock(),
                                            DummyObject,
                                            _json_cache=json_data_dict_one)
        
        json_data_list = [{"value": "test"}]
        self.objects_list = api.BaseList(Mock(),
                                         DummyObject,
                                         _json_cache=json_data_list)
        
    def test_objects_list(self):
        for item in self.many_objects_dict:
            assert item.value == "test"

        for item in self.one_object_dict:
            assert item.value == "test"

        for item in self.objects_list:
            assert item.value == "test"
    

class CompanyListTest(TestCase):
    def setUp(self):
        self.companies = api.CompanyList(Mock(),
                                         _json_cache=TEST_COMPANIES)

    def test_get_company_list(self):
        for company in self.companies:
            assert company.name == "Alice Cooper"
            assert company.reference == "123456"

    def test_company_count(self):
        assert len(self.companies) == 1


class JobListTest(TestCase):
    def setUp(self):        
        self.jobs = api.JobList(Mock(), _json_cache=TEST_JOBS)

    def test_job_list(self):
        for job in self.jobs:
            assert job.title == "Test Job"

    def test_job_count(self):
        assert len(self.jobs) == 1


class TeamListTest(TestCase):
    def setUp(self):
        self.teams = api.TeamList(Mock(), _json_cache=TEST_TEAMS)


    def test_team_list(self):
        for team in self.teams:
            assert team.name == "Alice Cooper"
            assert team.status == "active"

    def test_team_count(self):
        assert len(self.teams) == 1


class JobPosterTest(TestCase):
    def setUp(self):
        client = Mock()
        client.hr.get_companies.return_value = TEST_COMPANIES
        client.hr.get_jobs.return_value = TEST_JOBS
        client.hr.get_teams.return_value = TEST_TEAMS
        user = Mock()

        self.job_poster = api.JobPoster(user, client)

    def test_get_companies(self):
        for company in self.job_poster.companies:
            assert company.name == "Alice Cooper"            

    def test_get_jobs(self):
        for company in self.job_poster.companies:
            for job in self.job_poster.jobs(company):
                assert job.title == "Test Job"

    def test_get_teams(self):
        for team in self.job_poster.teams:
            assert team.name == "Alice Cooper"
