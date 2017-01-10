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

import amela.utils as utils

from amela.query import Query
from amela.enums import MetricType
from amela.enums import BucketType
from amela.entities import Author
from amela.entities import Commit
from amela.entities import Repo
from amela.entities import File
from amela.entities import Entity

def pretty_print(json_str):
    print('R=\n', utils.beautify(json_str))

def unique(entity, q=None):
    if q is None:
        q = Query(es_hosts=["http://127.0.0.1:9200"])
    q.metric(MetricType.unique_count, entity)
    return q

def avg(entity, q=None):
    if q is None:
        q = Query(es_hosts=["http://127.0.0.1:9200"])
    q.metric(MetricType.avg, entity)
    return q


def test():

    q = unique(Author)
    r = q.solve(Author)
    pretty_print(r.to_dict()['aggregations'])

    q = unique(Commit)
    r = q.solve(Commit)
    pretty_print(r.to_dict()['aggregations'])

    q = unique(Repo)
    r = q.solve(Repo)
    pretty_print(r.to_dict()['aggregations'])

    q = unique(Commit)
    q.group_by_terms(Repo)
    r = q.solve(Entity)
    pretty_print(r.to_dict()['aggregations'])

    q = unique(Commit)
    q = unique(Author, q)
    q = avg(File, q)
    q.group_by_terms(Repo)
    r = q.solve(Entity)
    pretty_print(r.to_dict()['aggregations'])



if __name__ == '__main__':
    test()
