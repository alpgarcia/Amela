import pandas as pd

from amela.query_metrics import UniqueCount
from amela.query_metrics import Average
from amela.query_buckets import TimeBucket
from amela.query_buckets import TermsBucket
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

def onion(search, entity1, entity2):
    """ onion returns the onion model of any type of entity
    The onion model is defined as the number of developers
    contributing up to a 80% of the code (core), regular
    (up to 95%) and casual (the other 5%).

    This onion model may be also applied to other circumstances
    such as the onion model for organizations or the onion
    model for people resolving tickets.

    This is in the end a study that measures how concentrated
    the activity is.

    :param search: Search object used for solving
    :param entity1: Entity used to aggregate information (eg: authors)
    :param entity2: Entity used for measuring that aggregation (eg: commits)
    :type search: amela.query.Search
    :type entity1: amela.entities.*
    :type entity2: amela.entities.*

    :returns: dictionary with three values: core, regular, casual
    :rtype: dictionary
    """

    s = search.bucket(TermsBucket(entity2))
    result = s.solve()

    #TODO: return all of the elements, and not a subset
    list_elements = result.to_dict()['aggregations']
    entity2_values = []
    entity1_values = []
    for bucket in list_elements['terms.'+entity2.field_name]['buckets']:
        entity1_values.append(bucket['doc_count'])
        entity2_values.append(bucket['key'])

    # Calculate the onion values
    df = pd.DataFrame({'key':entity2_values,
                       'doc_count': entity1_values})
    total = df['doc_count'].sum()
    percent_80 = total * 0.8
    percent_95 = total * 0.95
    core = 0
    core_sum = 0
    regular = 0
    regular_sum = 0
    casual = 0

    for value in entity1_values:
        if (percent_80 > core_sum):
            core = core + 1
            core_sum = core_sum + value
        elif percent_95 > regular_sum:
            regular = regular + 1
            regular_sum = regular_sum + value
        else:
            casual = casual + 1

    return {"core":core,
            "regular":regular,
            "casual":casual}
