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

sys.path.insert(0, '..')

import amela.utils as utils
import amela.operations as app

from amela.query import Query
from amela.query import Search
from amela.query_metrics import UniqueCount
from amela.query_metrics import Average
from amela.query_buckets import TermsBucket
from amela.entities import Author
from amela.entities import Commit
from amela.entities import Repo
from amela.entities import File
from amela.entities import Project

def pretty_print(json_str):
    print('R=\n', utils.beautify(json_str))

def test_query():

    print("Unique Count Authors")
    q = Query().metric(UniqueCount(Author))
    r = q.solve()
    pretty_print(r.to_dict()['aggregations'])

    print("Unique Count Commits")
    q = Query().metric(UniqueCount(Commit()))
    r = q.solve()
    pretty_print(r.to_dict()['aggregations'])

    print("Unique Count Repos")
    q = Query().metric(UniqueCount(Repo))
    r = q.solve()
    pretty_print(r.to_dict()['aggregations'])

    print("Unique Count Commits by Repo")
    q = Query().bucket(TermsBucket(Repo)).metric(UniqueCount(Commit()))
    r = q.solve()
    pretty_print(r.to_dict()['aggregations'])

    print("Unique Count Commits, Author and Avg Files by Repo")
    q = Query() \
        .bucket(TermsBucket(Repo)) \
        .metric(UniqueCount(Commit())) \
        .metric(UniqueCount(Author)) \
        .metric(Average(File()))
    r = q.solve()
    pretty_print(r.to_dict()['aggregations'])

    print("Bucketize by Repo and then by Commit")
    q = Query() \
        .bucket(TermsBucket(Repo)) \
        .bucket(TermsBucket(Commit()))
    r = q.solve()
    pretty_print(r.to_dict()['aggregations'])


def test_search():
    print("Unique Count Commits by Author by Month (Filtering Merges)")
    # Add Author bucketing to test only filter
    # (we should retrieve just Santis' bucket)
    s = Search(Commit(), Author())
    p = app.only(s, Author(), 'Santiago Dueñas')
    uc = app.unique_count(p)
    sp = app.split(uc)
    r = sp.solve()
    pretty_print(r.to_dict()['aggregations'])

    print("Unique Count Commits by Author by Month")
    s = Search(Commit(filter_merges=False))
    p = app.only(s, Author(), 'Santiago Dueñas')
    uc = app.unique_count(p)
    sp = app.split(uc)
    r = sp.solve()
    pretty_print(r.to_dict()['aggregations'])

    print("Unique Count Authors by Month")
    s = Search(Author())
    uc = app.unique_count(s)
    sp = app.split(uc)
    r = sp.solve()
    pretty_print(r.to_dict()['aggregations'])

    print("Average Files by Month")
    s = Search(File())
    uc = app.average(s)
    sp = app.split(uc)
    r = sp.solve()
    pretty_print(r.to_dict()['aggregations'])

    print("Onion Study")
    s = Search(Commit(), Author())
    result = app.onion(s, Commit(), Author())
    print(result)

    print("Commits per project")
    s = Search(Commit(), Project())
    aut = app.unique_count(s, entity=Author())
    org = app.unique_count(aut, entity=Repo())
    com = app.unique_count(org)
    r = com.solve()
    pretty_print(r.to_dict()['aggregations'])



def print_header(text):
    print("\n_________")
    print("\___ ___/")
    print("   | |   ", text)
    print("   |_|\n")

if __name__ == '__main__':
    print_header("QUERY TESTS")
    test_query()

    print_header("SEARCH TESTS")
    test_search()
