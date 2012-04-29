from unittest import TestCase
from mock import Mock

from candidates_emailer import api


### Test Data ###
TEST_COMPANIES = [{u'name': u'Alice Cooper',
                   u'owner_user_id': u'acooper',
                   u'reference': u'123456',
                   u'status': u'active'}]

TEST_ROLES = {u'userrole': [{u'affiliation_status': u'none',
                             u'company__name': u'Alice Cooper',
                             u'company__reference': u'123456',
                             u'engagement__reference': u'',
                             u'has_team_room_access': u'1',
                             u'is_owner': u'1',
                             u'parent_team__id': u'6yiq_pfanlnwclja9-smag',
                             u'parent_team__name': u'Alice Cooper',
                             u'parent_team__reference': u'123456',
                             u'permissions': {u'permission': [u'manage_finance',
                                                              u'manage_employment',
                                                              u'manage_recruiting',
                                                              u'manage_teamroom']},
                             u'reference': u'1918677',
                             u'role': u'admin',
                             u'team__id': u'6yiq_pfanlnwclja9-smag',
                             u'team__is_hidden': u'',
                             u'team__name': u'Alice Cooper',
                             u'team__reference': u'123456',
                             u'user__first_name': u'Alice',
                             u'user__id': u'acooper',
                             u'user__is_provider': u'1',
                             u'user__last_name': u'Cooper',
                             u'user__reference': u'1234567'},
                            {u'affiliation_status': u'none',
                             u'company__name': u'Acme Corp',
                             u'company__reference': u'123',
                             u'engagement__reference': u'456719',
                             u'has_team_room_access': u'1',
                             u'parent_team__id': u'acme',
                             u'parent_team__name': u'Acme',
                             u'parent_team__reference': u'123',
                             u'permissions': u'',
                             u'reference': u'98765432',
                             u'role': u'member',
                             u'team__id': u'acmecorp',
                             u'team__is_hidden': u'',
                             u'team__name': u'Acme Corp',
                             u'team__reference': u'4567',
                             u'user__first_name': u'Alice',
                             u'user__id': u'acooper',
                             u'user__is_provider': u'1',
                             u'user__last_name': u'Cooper',
                             u'user__reference': u'123567'}]}

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
        

TEST_OFFERS = {u'lister': {u'paging': {u'count': u'20', u'offset': u'0'},
                           u'query': u'',
                           u'sort': u'',
                           u'total_items': u'1'},
               u'offer': {u'buyer_company__name': u'Alice Cooper',
                          u'buyer_company__reference': u'123456',
                          u'buyer_team__id': u'6yiq_pfanlnwclja9-smag',
                          u'buyer_team__name': u'Alice Cooper',
                          u'buyer_team__reference': u'123456',
                          u'candidacy_status': u'rejected',
                          u'created_by': u'acooper',
                          u'created_by_name': u'Alice Cooper',
                          u'created_time': u'1334669594000',
                          u'created_type': u'buyer',
                          u'engagement__reference': u'',
                          u'engagement_end_date': u'1334620800000',
                          u'engagement_job_type': u'hourly',
                          u'engagement_start_date': u'1334620800000',
                          u'engagement_title': u'',
                          u'estimated_duration': u'Ongoing / More than 6 months',
                          u'estimated_duration_id': u'1',
                          u'has_buyer_signed': u'',
                          u'has_provider_signed': u'',
                          u'hourly_charge_rate': u'55.56',
                          u'hourly_pay_rate': u'50',
                          u'interview_status': u'waiting_for_provider',
                          u'is_hidden': u'1',
                          u'is_matching_preferences': u'1',
                          u'is_shortlisted': u'',
                          u'is_undecided': u'0',
                          u'is_viewed': u'',
                          u'job__reference': u'1234567',
                          u'job__title': u'Test Job',
                          u'key': u'~~abb3808faeb2a533',
                          u'modified_time': u'1334712930000',
                          u'my_role': u'both',
                          u'provider__has_agency': u'',
                          u'provider__id': u'bbobberson',
                          u'provider__name': u'Bob Bobberson',
                          u'provider__profile_url': u'https://www.odesk.com/users/~~ciphertext',
                          u'provider__reference': u'7654321',
                          u'provider_team__reference': u'',
                          u'reference': u'1234567',
                          u'rent_percent': u'10',
                          u'roles': {u'role': [u'provider', u'buyer']},
                          u'status': u'',
                          u'weekly_hours_limit': u'',
                          u'weekly_salary_charge_amount': u'',
                          u'weekly_salary_pay_amount': u'',
                          u'weekly_stipend_hours': u''}}


class BaseAPIObjectTest(TestCase):
    def setUp(self):
        self.object = api.BaseAPIObject({"num_int_value": "1",
                                         "num_value_hours": "1.2",
                                         "is_truth_value": "1",
                                         "is_false_value": "",
                                         "string_value": "some value"})

    def test_get_string_field(self):
        self.assertEquals(self.object.string_value, "some value")

    def test_get_boolean_field_true(self):
        self.assertTrue(self.object.is_truth_value)

    def test_get_boolean_field_false(self):
        self.assertFalse(self.object.is_false_value)

    def test_get_num_int_field(self):
        self.assertIsInstance(self.object.num_int_value, int)

    def test_get_num_float_field(self):
        self.assertIsInstance(self.object.num_value_hours, float)


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
            self.assertEquals(item.value, "test")

        for item in self.one_object_dict:
            self.assertEquals(item.value, "test")

        for item in self.objects_list:
            self.assertEquals(item.value, "test")

    def test_objects_index(self):
        item = self.many_objects_dict[0]
        self.assertEquals(item.value, "test")

        item = self.one_object_dict[0]
        self.assertEquals(item.value, "test")

        item = self.objects_list[0]
        self.assertEquals(item.value, "test")
    

class CompanyListTest(TestCase):
    def setUp(self):
        self.companies = api.CompanyList(Mock(),
                                         _json_cache=TEST_COMPANIES)

    def test_get_company_list(self):
        for company in self.companies:
            self.assertEquals(company.name, "Alice Cooper")
            self.assertEquals(company.reference, "123456")

    def test_company_count(self):
        self.assertEquals(len(self.companies), 1)

    def test_company_index(self):
        company = self.companies[0]
        self.assertEquals(company.name, "Alice Cooper")


class JobListTest(TestCase):
    def setUp(self):        
        self.jobs = api.JobList(Mock(), _json_cache=TEST_JOBS)

    def test_job_list(self):
        for job in self.jobs:
            self.assertEquals(job.title, "Test Job")

    def test_job_count(self):
        self.assertEquals(len(self.jobs), 1)

    def test_job_index(self):
        job = self.jobs[0]
        self.assertEquals(job.title, "Test Job")


class TeamListTest(TestCase):
    def setUp(self):
        self.teams = api.TeamList(Mock(), _json_cache=TEST_TEAMS)


    def test_team_list(self):
        for team in self.teams:
            self.assertEquals(team.name, "Alice Cooper")
            self.assertEquals(team.status, "active")

    def test_team_count(self):
        self.assertEquals(len(self.teams), 1)

    def test_team_index(self):
        team = self.teams[0]
        self.assertEquals(team.name, "Alice Cooper")


class OfferListTest(TestCase):
    def setUp(self):
        self.offers = api.OfferList(Mock(), _json_cache=TEST_OFFERS)

    def test_offer_list(self):
        for offer in self.offers:
            self.assertEquals(offer.provider__name, "Bob Bobberson")
            self.assertEquals(offer.provider__id, "bbobberson")

    def test_offer_count(self):
        self.assertEquals(len(self.offers), 1)

    def test_offers_index(self):
        offer = self.offers[0]
        self.assertEquals(offer.provider__name, "Bob Bobberson")


class UserRoleListTest(TestCase):
    def setUp(self):
        self.roles = api.UserRoleList(Mock(), _json_cache=TEST_ROLES)

    def test_role_list(self):
        for role in self.roles:
            self.assertEquals(role.user__first_name, "Alice")

    def test_role_count(self):
        self.assertEquals(len(self.roles), 2)

    def test_role_index(self):
        role = self.roles[1]
        self.assertEquals(role.company__name, "Acme Corp")

        
class JobPosterTest(TestCase):
    def setUp(self):
        client = Mock()
        client.hr.get_companies.return_value = TEST_COMPANIES
        client.hr.get_jobs.return_value = TEST_JOBS
        client.hr.get_teams.return_value = TEST_TEAMS
        client.hr.get_offers.return_value = TEST_OFFERS
        user = Mock()

        self.job_poster = api.JobPoster(user, client)

    def test_get_companies(self):
        for company in self.job_poster.companies:
            self.assertEquals(company.name, "Alice Cooper")

    def test_get_jobs(self):
        for company in self.job_poster.companies:
            for job in self.job_poster.jobs(company):
                self.assertEquals(job.title, "Test Job")

    def test_get_teams(self):
        for team in self.job_poster.teams:
            self.assertEquals(team.name, "Alice Cooper")

    def test_get_offers(self):
        for company in self.job_poster.companies:
            for job in self.job_poster.jobs(company):
                for offer in self.job_poster.offers(job):
                    self.assertEquals(offer.provider__name, "Bob Bobberson")
