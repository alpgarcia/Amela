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

import elasticsearch
import elasticsearch_dsl

from .filters.terms_filter import TermFilter


class Metric:
    """
    AMELA: Abstract MEtric LAyer

    All metrics should be created on top of Metric
    abstraction.
    """

    def __init__(self, es_hosts, index_name):
        client = elasticsearch.Elasticsearch(es_hosts)
        self.__s = elasticsearch_dsl.Search(using=client, index=index_name)

    def filter(self, f):
        '''Adds a given filter to the query. Up to now
        it only understands term filters
        '''
        if f.type == TermFilter.TYPE:
            f_dict = { f.field_name : [f.field_value] }
            print(f_dict)
            self.__s = self.__s.filter(f.type, ** f_dict)
            print(self.__s.to_dict())

        return self

    def execute(self):
        return self.__s.execute()
