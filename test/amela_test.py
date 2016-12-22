# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 Bitergia
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
# Authors:
#   Daniel Izquierdo Cortazar <dizquierdo@bitergia.com>
#   Alberto Pérez García-Plaza <alpgarcia@bitergia.com>
#


import sys
from datetime import datetime

sys.path.insert(0, '..')

import amela.filters
import amela.query
import amela.utils

# Test script on how to build metrics with Amela module
# We'd try to solve at least the following combinations:
#
# - unique_count.filter
# - [filter].groupByQuarter.unique_count
# - [filter].groupByTerms.unique_count
# - [filter].[filter]groupByTerms.groupByTerms.unique_count
#
# Also we'll test all methods from:
#  https://github.com/dicortazar/ipython-notebooks/blob/master/others/Metrics%20with%20ElasticSearch%20DSL.ipynb
#

# TODO these constants should be stored in a file
#      we could have a different file for each data source
#      or a separate dictionary for each data source,
#      or even just a single dictionary with data source
#      names as keys and other dicts as values.
MESSAGE_ANALYZED_FIELD_NAME = 'message_analyzed'
FILES_FIELD_NAME = 'files'
COMMIT_ID_FIELD_NAME = 'hash'
AUTHOR_DATE_FIELD_NAME = 'author_date'
AUTHOR_NAME_FIELD_NAME = 'author_name'
REPO_NAME_FIELD_NAME = 'repo_name'

terms_filter = amela.filters.Terms( \
    field_name=MESSAGE_ANALYZED_FIELD_NAME, \
    field_value=['merge'])

gt_filter = amela.filters.GreaterThan( \
    field_name=FILES_FIELD_NAME, \
    n=0)

gt_date_filter = amela.filters.GreaterThan( \
    field_name=AUTHOR_DATE_FIELD_NAME, \
    n=datetime(2016, 1, 1))


def create_query():
    q = amela.query.Query(es_hosts=["http://127.0.0.1:9200"])
    return q.search(index_name='git')


def pretty_print(json_str):
    print('R=\n', amela.utils.beautify(json_str))


def terms_filter_test():
    """
    Search for messages that contain 'merge'
    """
    print('MERGES FILTER:')

    r = create_query() \
        .filter(terms_filter) \
        .execute()
    #  print just a quick summary
    pretty_print(r.to_dict()['hits']['total'])


def unique_commits_test():
    """
    Count Unique Commits
    """
    print('\n\nCOUNTING UNIQUE COMMITS:')

    # Each time we call search, we create a new search query
    r = create_query() \
        .unique_count(name='commits', field=COMMIT_ID_FIELD_NAME) \
        .execute()
    pretty_print(r.to_dict()['aggregations'])


def unique_commits_filtered_by_terms_test():
    """
    Filter by terms and then count unique commits
    """
    print('\n\nTERMS FILTERING AND THEN COUNT UNIQUE COMMITS')

    r = create_query() \
        .unique_count(name='commits',field=COMMIT_ID_FIELD_NAME) \
        .filter(terms_filter) \
        .execute()
    pretty_print(r.to_dict()['aggregations'])


def unique_commits_ignore_merges_test():
    """
    Count unique commits excluding merges
    """
    print('\n\nCOUNTING UNIQUE COMMITS AND IGNORING MERGES')

    r = create_query() \
        .unique_count(name='commits', field=COMMIT_ID_FIELD_NAME) \
        .filter(gt_filter) \
        .execute()
    pretty_print(r.to_dict()['aggregations'])


def unique_count_filtered_by_date_test():
    """
    Filter by date and then count unique commits
    """
    print('\n\nDATE FILTERING AND THEN COUNT UNIQUE COMMITS')

    r = create_query() \
        .filter(gt_date_filter) \
        .unique_count(name='commits',field=COMMIT_ID_FIELD_NAME) \
        .execute()
    pretty_print(r.to_dict()['aggregations'])


def count_grouped_by_quarters_test():
    """
    Group by quarters and then count commits
    """
    print('\n\nGROUP BY QUARTERS AND THEN COUNT COMMITS')

    r = create_query() \
        .group_by_quarters(name='histogram', field=AUTHOR_DATE_FIELD_NAME) \
        .execute()
    pretty_print(r.to_dict()['aggregations'])


def unique_count_grouped_by_quarters_test():
    """
    Group by quarters and then count unique commits
    """
    print('\n\nGROUP BY QUARTERS AND THEN COUNT UNIQUE COMMITS')

    r = create_query() \
        .group_by_quarters(name='histogram', field=AUTHOR_DATE_FIELD_NAME) \
        .unique_count(name='commits',field=COMMIT_ID_FIELD_NAME, \
            parent='histogram') \
        .execute()
    pretty_print(r.to_dict()['aggregations'])


def count_filtered_and_grouped_by_quarters_test():
    """
    Filter by date, group by quarters and then count commits
    """
    print('\n\nDATE FILTERING, GROUP BY QUARTERS AND THEN COUNT COMMITS')

    r = create_query() \
        .filter(gt_date_filter) \
        .group_by_quarters(name='histogram', field=AUTHOR_DATE_FIELD_NAME) \
        .execute()
    pretty_print(r.to_dict()['aggregations'])


def unique_count_filtered_and_grouped_by_quarters_test():
    """
    Filter by date, group by quarters and then count unique commits
    """
    print('\n\nDATE FILTERING, GROUP BY QUARTERS AND THEN COUNT UNIQUE COMMITS')

    r = create_query() \
        .filter(gt_date_filter) \
        .group_by_quarters(name='histogram', field=AUTHOR_DATE_FIELD_NAME) \
        .unique_count(name='commits',field=COMMIT_ID_FIELD_NAME, \
            parent='histogram') \
        .execute()
    pretty_print(r.to_dict()['aggregations'])


def unique_count_grouped_by_terms_test():
    """
    Group by terms and then count unique commits
    """
    print('\n\nGROUP BY TERMS AND THEN COUNT UNIQUE COMMITS')

    r = create_query() \
        .group_by_terms(name='by_repo', field=REPO_NAME_FIELD_NAME) \
        .unique_count(name='commits',field=COMMIT_ID_FIELD_NAME, \
            parent='by_repo') \
        .execute()
    pretty_print(r.to_dict()['aggregations'])


def unique_count_filtered_and_grouped_by_terms_test():
    """
    Filter by date, group by terms and then count unique commits
    """
    print('\n\nDATE FILTERING, GROUP BY TERMS AND THEN COUNT UNIQUE COMMITS')

    r = create_query() \
        .filter(gt_date_filter) \
        .group_by_terms(name='by_author', field=AUTHOR_NAME_FIELD_NAME) \
        .unique_count(name='commits',field=COMMIT_ID_FIELD_NAME, \
            parent='by_author') \
        .execute()
    pretty_print(r.to_dict()['aggregations'])


def unique_count_grouped_by_terms_twice_test():
    """
    Group by terms twice and then count unique commits
    """
    print('\n\nGROUP BY TERMS TWICE AND THEN COUNT UNIQUE COMMITS')

    r = create_query() \
        .group_by_terms(name='by_repo', field=REPO_NAME_FIELD_NAME) \
        .group_by_terms(name='by_author', field=AUTHOR_NAME_FIELD_NAME, \
            parent='by_repo') \
        .unique_count(name='commits',field=COMMIT_ID_FIELD_NAME, \
            parent='by_repo.by_author') \
        .execute()
    pretty_print(r.to_dict()['aggregations'])


def unique_count_filtered_grouped_by_terms_twice_test():
    """
    Filter by date, group by terms twice and then count unique commits
    """
    print('\n\nFILTER BY DATE, GROUP BY TERMS TWICE AND THEN COUNT UNIQUE COMMITS')

    r = create_query() \
        .filter(gt_date_filter) \
        .group_by_terms(name='by_repo', field=REPO_NAME_FIELD_NAME) \
        .group_by_terms(name='by_author', field=AUTHOR_NAME_FIELD_NAME, \
            parent='by_repo') \
        .unique_count(name='commits',field=COMMIT_ID_FIELD_NAME, \
            parent='by_repo.by_author') \
        .execute()
    pretty_print(r.to_dict()['aggregations'])


if __name__ == '__main__':
    terms_filter_test()
    unique_commits_test()
    unique_commits_filtered_by_terms_test()
    unique_commits_ignore_merges_test()
    unique_count_filtered_by_date_test()
    count_grouped_by_quarters_test()
    unique_count_grouped_by_quarters_test()
    count_filtered_and_grouped_by_quarters_test()
    unique_count_filtered_and_grouped_by_quarters_test()
    unique_count_grouped_by_terms_test()
    unique_count_filtered_and_grouped_by_terms_test()
    unique_count_grouped_by_terms_twice_test()
    unique_count_filtered_grouped_by_terms_twice_test()
