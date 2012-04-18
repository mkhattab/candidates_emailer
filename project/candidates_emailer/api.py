import re

__all__ = ["Job",
           "Team",
           "Company",
           "Offer",
           "JobList",
           "TeamList",
           "CompanyList",
           "OfferList",
           "JobPoster"]

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
    
    def __init__(self, _json_cache=None):
        super(Company, self).__init__(_json_cache)


class Job(BaseAPIObject):
    type = "job"
    
    def __init__(self, _json_cache=None):
        super(Job, self).__init__(_json_cache)


class Team(BaseAPIObject):
    type = "team"
    
    def __init__(self, _json_cache=None):
        super(Team, self).__init__(_json_cache)


class Offer(BaseAPIObject):
    type = "offer"

    def __init__(self, _json_cache=None):
        super(Offer, self).__init__(_json_cache)


class BaseList(object):
    def __init__(self, client, object_cls, _json_cache=None):
        self.client = client
        self._json_cache = _json_cache
        self.object_cls = object_cls
        self.lister = None

        if not _json_cache:
            self.objects = []
        
        if isinstance(_json_cache, dict):
            self.lister = _json_cache["lister"]
            objects = _json_cache[self.object_cls.type]            
            if isinstance(objects, list):
                self.objects = objects
            else:
                self.objects = [objects]
        elif isinstance(_json_cache, list):
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
    def __init__(self, client, _json_cache=None):
        super(TeamList, self).__init__(client,
                                       Team,
                                       _json_cache=_json_cache)
        
    
class CompanyList(BaseList):
    def __init__(self, client, _json_cache=None):
        super(CompanyList, self).__init__(client,
                                          Company,
                                          _json_cache=_json_cache)


class JobList(BaseList):
    def __init__(self, client, _json_cache=None):
        super(JobList, self).__init__(client,
                                       Job,
                                       _json_cache=_json_cache)


class OfferList(BaseList):
    def __init__(self, client, _json_cache=None):
        super(OfferList, self).__init__(client,
                                       Offer,
                                       _json_cache=_json_cache)

class JobPoster(object):
    def __init__(self, user, client):    
        self.user = user
        self.client = client
        self._companies = None
        self._teams = None
        self._jobs = {}
        self._offers = {}

    @property
    def companies(self):
        if self._companies:
            return self._companies
        else:
            data = self._get_companies()
            self._companies = CompanyList(self.client,
                                          _json_cache=data)
            return self._companies

    @property
    def teams(self):
        if self._teams:
            return self._teams
        else:
            data  = self._get_teams()
            self._teams = TeamList(self.client,
                                   _json_cache=data)
            return self._teams

    def jobs(self, company):
        try:
            return self._jobs[company.reference]
        except KeyError:
            data = self._get_jobs(buyer_team_reference=company.reference)
            jobs = JobList(self.client,
                           _json_cache=data)
            self._jobs[company.reference] = jobs
            return jobs

    def offers(self, job):
        try:
            return self._offers[job.reference]
        except KeyError:
            data = self._get_offers(
                buyer_team_reference=job.buyer_team__reference,
                job_ref=job.reference)
            offers = OfferList(self.client, _json_cache=data)
            self._offers[job.reference] = offers
            return offers
        
    def _get_companies(self):
        return self.client.hr.get_companies()

    def _get_jobs(self, **kwargs):
        return self.client.hr.get_jobs(**kwargs)

    def _get_teams(self):
        return self.client.hr.get_teams()

    def _get_offers(self, **kwargs):
        return self.client.hr.get_offers(**kwargs)
