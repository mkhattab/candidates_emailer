import re

INT_VALUE_FIELD_REGEX = (
    "(^num_)",
)
FLOAT_VALUE_FIELD_REGEX = (
    "(_hours$)",
)
BOOLEAN_VALUE_FIELD_REGEX = (
    "(^is_)",
)
_int_class_re = re.compile(r"|".join(INT_VALUE_FIELD_REGEX))
_float_class_re = re.compile(r"|".join(FLOAT_VALUE_FIELD_REGEX))
_boolean_class_re = re.compile(r"|".join(BOOLEAN_VALUE_FIELD_REGEX))


class FieldConversionError(Exception):
    pass

class AccessTokensRequiredError(Exception):
    pass


class BaseAPIObject(object):
    def __init__(self, _json_cache={}):
        self._json_cache = _json_cache

    def __getattr__(self, name):
        try:
            return self._try_convert_field(name, self._json_cache[name])
        except KeyError:
            raise AttributeError("That field does not exist")

    def _try_convert_field(self, field, val):
        try:
            if _int_class_re.match(field):
                try:
                    return int(val, 10)
                except ValueError:
                    try:
                        return float(val)
                    except ValueError:
                        raise FieldConversionError
            if _float_class_re.match(field):
                try:
                    return float(val)
                except ValueError:
                    raise FieldConversionError

            if _boolean_class_re.match(field):
                try:
                    return bool(val)
                except ValueError:
                    raise FieldConversionError

            return val
        except FieldConversionError:
            return val


class Company(BaseAPIObject):
    def __init__(self, _json_cache={}):
        super(BaseAPIObject, self).__init__(client, _json_cache)


class Job(BaseAPIObject):
    def __init__(self, _json_cache={}):
        super(BaseAPIObject, self).__init__(client, _json_cache)


class Team(BaseAPIObject):
    def __init__(self, _json_cache={}):
        super(BaseAPIObject, self).__init__(client, _json_cache)


class BaseList(object):
    def __init__(self, client, _json_cache={}):
        pass

    def __iter__(self):
        return self

    def __next__(self):
        raise StopIteration


class TeamList(object):
    pass


class CompanyList(object):
    pass


class JobList(object):
    pass


class JobPoster(object):

    def __init__(self, user, client):    
        self.user = user
        self.client = client

    def _get_companies(self):
        pass

    def _get_jobs(self):
        pass

    def _get_teams(self):
        pass
