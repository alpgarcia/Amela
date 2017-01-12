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

"""
AMELA: Abstract MEtric LAyer

All metrics should be created on top of Metric
abstraction.
"""
import copy
import elasticsearch
import elasticsearch_dsl

import amela.utils as utils

from amela.query_buckets import TermsBucket
from amela.query_metrics import UniqueCount
from amela.query_metrics import Average


class Query:
    """
    Base class for building Queries
    """

    def __init__(self, entity = None):
        self.__aggs = []
        self.__metrics = []
        self.__filters = []
        self.__entity  = entity

    def metric(self, metric):
        self.__metrics.append(metric)
        return self

    def bucket(self, bucket):
        self.__aggs.append(bucket)
        return self

    def filter(self, fil):
        self.__filters.append(fil)
        return self

    def clone(self):
        return copy.deepcopy(self)

    def solve(self):

        db =  {
            'es_hosts' : ["http://127.0.0.1:9200"],
            'dbname' : 'git'
        }

        client = elasticsearch.Elasticsearch(db['es_hosts'])
        s = elasticsearch_dsl.Search(using=client, index=db['dbname'])

        # Filters are applied directly over DSL Search object
        for fil in self.__filters:
            s = fil.solve(s, self.__entity)

        # Once filters are associated to Search object we can get_name
        # a ref to aggs part and add all aggregations to that point
        parent_bucket = s.aggs

        for bucket in self.__aggs:
            parent_bucket = bucket.solve(parent_bucket, self.__entity)

        for metric in self.__metrics:
            metric.solve(parent_bucket, self.__entity)

        # TODO print query in debug mode
        print('Q=\n', utils.beautify(s.to_dict()))
        return s.execute()


class Search(Query):

    def __init__(self, entity, *term_buckets_entities):
        super().__init__(entity)

        for fil in entity.filters:
            self.filter(fil)

        for eb in term_buckets_entities:
            self.bucket(TermsBucket(eb))



    ## OLD METHODS

    # def search(self, index_name):
    #     """ Reset Query by creating a new search object
    #     """
    #     self.__s = elasticsearch_dsl.Search(using=self.__client, index=index_name)
    #     return self
    #
    # def unique_count(self, name, field, parent=None):
    #     """ Count unique values in a field
    #     """
    #     if parent is None:
    #         self.__s.aggs.metric(name, 'cardinality', field=field,
    #             precision_threshold=self.PRECISION)
    #     else:
    #         a = self.__s
    #         for ancestor in parent.split('.'):
    #             a = a.aggs[ancestor]
    #         a.metric(name, 'cardinality', field=field,
    #             precision_threshold=self.PRECISION)
    #
    #     return self
    #
    # def group_by_quarters(self, name, field, parent=None):
    #     """ Bucketize data in quarters
    #     """
    #     if parent is None:
    #         self.__s.aggs.bucket(name, 'date_histogram', \
    #             field=field, interval='quarter')
    #     else:
    #         a = self.__s
    #         for ancestor in parent.split('.'):
    #             a = a.aggs[ancestor]
    #         a.bucket(name, 'date_histogram', \
    #             field=field, interval='quarter')
    #
    #     return self
    #
    # def group_by_terms(self, name, field, parent=None):
    #     """ Bucketize data by terms
    #     """
    #     if parent is None:
    #         self.__s.aggs.bucket(name, 'terms', field=field)
    #     else:
    #         a = self.__s
    #         for ancestor in parent.split('.'):
    #             a = a.aggs[ancestor]
    #         a.bucket(name, 'terms', field=field)
    #
    #     return self
    #
    # def filter(self, custom_filter):
    #     """Adds a given filter to the query.
    #     """
    #     f_dict = {custom_filter.field_name() : custom_filter.field_value()}
    #
    #     self.__s = self.__s.filter(custom_filter.type(), ** f_dict)
    #
    #     return self
    #
    # def execute(self):
    #     """ Execute query
    #     """
    #     # TODO print query in debug mode
    #     print('Q=\n', utils.beautify(self.__s.to_dict()))
    #     return self.__s.execute()
