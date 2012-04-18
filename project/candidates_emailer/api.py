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
    def __init__(self, _json_cache=None):
        self._json_cache = _json_cache

    def __getattr__(self, name):
        if not self._json_cache: raise AttributeError("That field does not exist")
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
    type = "company"
    
    def __init__(self, _json_cache={}):
        super(Company, self).__init__(_json_cache)


class Job(BaseAPIObject):
    type = "job"
    
    def __init__(self, _json_cache={}):
        super(Job, self).__init__(_json_cache)


class Team(BaseAPIObject):
    type = "team"
    
    def __init__(self, _json_cache={}):
        super(Team, self).__init__(_json_cache)


class BaseList(object):
    def __init__(self, client, object_cls, _json_cache={}):
        self.client = client
        self._json_cache = _json_cache
        self.object_cls = object_cls
        if isinstance(_json_cache, dict):
            self.lister = _json_cache["lister"]
            objects = _json_cache[self.object_cls.type]            
            if isinstance(objects, list):
                self.objects = objects
            else:
                self.objects = [objects]
        elif isinstance(_json_cache, list):
            self.lister = None
            self.objects = _json_cache

    def __len__(self):
        if self.lister:
            return int(self.lister["total_items"], 10)
        else:
            return len(self.objects)
    
    def __iter__(self):
        self._index = 0
        self._page = 0
        return self

    def next(self):
        if self._index > len(self):            
            raise StopIteration
        try:
            _json = self.objects[self._index]
        except IndexError:
            raise StopIteration
        
        self._index += 1
        return self.object_cls(_json_cache=_json)


class TeamList(BaseList):
    def __init__(self, client, _json_cache={}):
        super(TeamList, self).__init__(client,
                                       Team,
                                       _json_cache=_json_cache)
        
    
class CompanyList(BaseList):
    def __init__(self, client, _json_cache={}):
        super(CompanyList, self).__init__(client,
                                          Company,
                                          _json_cache=_json_cache)


class JobList(BaseList):
    def __init__(self, client, _json_cache={}):
        super(JobList, self).__init__(client,
                                       Job,
                                       _json_cache=_json_cache)



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
