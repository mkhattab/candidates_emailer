from unittest import TestCase
from mock import Mock

from candidates_emailer import api

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
    
