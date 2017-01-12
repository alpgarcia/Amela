
from amela.query_metrics import UniqueCount
from amela.query_metrics import Average
from amela.query_buckets import TimeBucket
from amela.enums import Interval


def unique_count(search, entity=None):
    s = search.clone()
    s.metric(UniqueCount(entity))
    return s

def average(search, entity=None):
    s = search.clone()
    s.metric(Average(entity))
    return s

def split(search, entity=None, interval=Interval.month):
    s = search.clone()
    s.bucket(TimeBucket(entity, interval))
    return s

def table(search):
    pass

def ts(search, entity):
    pass
