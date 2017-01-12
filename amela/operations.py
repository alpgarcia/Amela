
from amela.query_metrics import UniqueCount
from amela.query_metrics import Average
from amela.query_buckets import TimeBucket
from amela.query_filters import TermsFilter
from amela.enums import Interval


def unique_count(search, entity=None):
    s = search.clone()
    return s.metric(UniqueCount(entity))

def average(search, entity=None):
    s = search.clone()
    return s.metric(Average(entity))

def split(search, entity=None, interval=Interval.month):
    s = search.clone()
    return s.bucket(TimeBucket(entity, interval))

def only(search, entity=None, terms='*'):
    s = search.clone()
    return s.filter(TermsFilter(entity, terms))

def table(search):
    pass

def ts(search, entity):
    pass
