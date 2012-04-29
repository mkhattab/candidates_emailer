import re

__all__ = ["Job",
           "Team",
           "Company",
           "Offer",
           "UserRole",
           "JobList",
           "TeamList",
           "UserRoleList",
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
    

class Job(BaseAPIObject):
    type = "job"


class Team(BaseAPIObject):
    type = "team"
    

class Offer(BaseAPIObject):
    type = "offer"


class UserRole(BaseAPIObject):
    type = "userrole"
    

class BaseList(object):
    def __init__(self, client, object_cls, _json_cache=None):
        self.client = client
        self._json_cache = _json_cache
        self.object_cls = object_cls
        self.lister = None

        if not _json_cache:
            self.objects = []
        
        if isinstance(_json_cache, dict):
            try:
                self.lister = _json_cache["lister"]
            except KeyError:
                self.lister = None                
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

    def __getitem__(self, key):
        if not isinstance(key, int):
            raise IndexError("list indices must be integers, not str")

        if key > len(self):
            raise IndexError("list index out of range")
        try:
            return self.object_cls(_json_cache=self.objects[key])
        except IndexError:
            raise NotImplementedError("Paging has not been implemented yet")

    def __delitem__(self, key):
        if not isinstance(key, int):
            raise IndexError("list indices must be integers, not str")

        length = len(self)
        if key > length:
            raise IndexError("list assignment out of range")

        try:
            del self.objects[key]
            if self.lister:
                self.lister['total_items'] = str(length - 1)
        except IndexError:
            raise NotImplementedError("Paging has not been implemented yet")

        
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


class UserRoleList(BaseList):
    def __init__(self, client, _json_cache=None):
        super(UserRoleList, self).__init__(client,
                                       UserRole,
                                       _json_cache=_json_cache)

    def has_permissions(self, company, permissions):
        for role in self.__iter__():
            if role.company__reference == company.reference:
                if role.permissions:
                    return all(perm in role.permissions['permission']
                               for perm in permissions)
                else:
                    return False

        
class JobPoster(object):
    def __init__(self, user, client):    
        self.user = user
        self.client = client
        self._companies = None
        self._teams = None
        self._jobs = {}
        self._offers = {}
        self._roles = {}

    @property
    def companies(self):
        if not self._roles:
            self._roles = UserRoleList(self.client,
                                       _json_cache=self._get_user_roles())
        if self._companies:
            return self._companies
        else:
            data = self._get_companies()
            self._companies = CompanyList(self.client,
                                          _json_cache=data)
            for idx, company in enumerate(self._companies):
                if not self._roles.has_permissions(company,
                                                   ['manage_recruiting', 'manage_employment']):
                    del self._companies[idx]
                    
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

    def _get_user_roles(self):
        return self.client.hr.get_user_roles()
    
    def _get_companies(self):
        return self.client.hr.get_companies()

    def _get_jobs(self, **kwargs):
        return self.client.hr.get_jobs(**kwargs)

    def _get_teams(self):
        return self.client.hr.get_teams()

    def _get_offers(self, **kwargs):
        return self.client.hr.get_offers(**kwargs)
