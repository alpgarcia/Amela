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

import elasticsearch
import elasticsearch_dsl

import amela.utils as utils

from amela.enums import MetricType
from amela.enums import BucketType


class Query:
    """
    Base class for building Queries
    """

    METRIC = 'metric'
    ENTITY = 'entity'
    AGG_TYPE = 'type'

    PRECISION = 3000

    def __init__(self, es_hosts):
        self.__client = elasticsearch.Elasticsearch(es_hosts)
        self.__s = None
        self.__aggs = []
        self.__metrics = []

    def metric(self, metric_type, entity):
        self.__metrics.append({self.METRIC: metric_type, self.ENTITY: entity})

    def group_by_date(self, entity, interval):
        pass

    def group_by_terms(self, entity):
        self.__aggs.append({self.AGG_TYPE: BucketType.terms, self.ENTITY: entity})

    def solve(self, entity):

        s = elasticsearch_dsl.Search(using=self.__client, index=entity.index_name)

        parent_bucket = s.aggs
        for agg in self.__aggs:
            btype = agg[self.AGG_TYPE]
            field_name = agg[self.ENTITY].field_name
            name = btype.name + '.' + field_name

            if btype == BucketType.terms:
                parent_bucket = parent_bucket.bucket(name, 'terms',
                    field=field_name)

            elif btype == BucketType.date:
                pass

        for metric in self.__metrics:
            mtype = metric[self.METRIC]
            field_name = metric[self.ENTITY].field_name
            name = mtype.name + '.' + field_name

            if mtype == MetricType.unique_count:
                parent_bucket.metric(name, 'cardinality',
                    field=field_name,
                    precision_threshold=self.PRECISION)

            elif mtype == MetricType.avg:
                parent_bucket.metric(name, 'avg',
                    field=field_name)



        # TODO print query in debug mode
        #print('Q=\n', s.to_dict())
        print('Q=\n', utils.beautify(s.to_dict()))
        return s.execute()


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
