from unittest import TestCase

from candidates_emailer import api

class BaseAPIObjectTest(TestCase):
    def setUp(self):
        self.object = api.BaseAPIObject(None, {"num_int_value": "1",
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
