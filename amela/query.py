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

import amela.utils

class Query:
    """
    Base class for building Queries
    """

    PRECISION=3000

    def __init__(self, es_hosts):
        self.__client = elasticsearch.Elasticsearch(es_hosts)
        self.__s = None

    def search(self, index_name):
        """ Reset Query by creating a new search object
        """
        self.__s = elasticsearch_dsl.Search(using=self.__client, index=index_name)
        return self

    def unique_count(self, name, field, parent=None):
        """ Count unique values in a field
        """
        if parent is None:
            self.__s.aggs.metric(name, 'cardinality', field=field,
                precision_threshold=self.PRECISION)
        else:
            a = self.__s
            for ancestor in parent.split('.'):
                a = a.aggs[ancestor]
            a.metric(name, 'cardinality', field=field,
                precision_threshold=self.PRECISION)

        return self

    def group_by_quarters(self, name, field, parent=None):
        """ Bucketize data in quarters
        """
        if parent is None:
            self.__s.aggs.bucket(name, 'date_histogram', \
                field=field, interval='quarter')
        else:
            a = self.__s
            for ancestor in parent.split('.'):
                a = a.aggs[ancestor]
            a.bucket(name, 'date_histogram', \
                field=field, interval='quarter')

        return self

    def group_by_terms(self, name, field, parent=None):
        """ Bucketize data by terms
        """
        if parent is None:
            self.__s.aggs.bucket(name, 'terms', field=field)
        else:
            a = self.__s
            for ancestor in parent.split('.'):
                a = a.aggs[ancestor]
            a.bucket(name, 'terms', field=field)

        return self

    def filter(self, custom_filter):
        """Adds a given filter to the query.
        """
        f_dict = {custom_filter.field_name() : custom_filter.field_value()}

        self.__s = self.__s.filter(custom_filter.type(), ** f_dict)

        return self

    def execute(self):
        """ Execute query
        """
        # TODO print query in debug mode
        print('Q=\n', amela.utils.beautify(self.__s.to_dict()))
        return self.__s.execute()
