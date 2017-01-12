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


class Filter:
    """
    Generic Filter
    """
    filter_type = None

    def __init__(self, entity, field_value):
        self.entity = entity
        self.field_value = field_value
        self._kwargs = {}

    def get_field_name(self):
        return self.entity.field_name

    def fill_args(self):
        self._kwargs[self.get_field_name()] = self.field_value

    def solve(self, search, entity):
        if self.entity is None:
            self.entity = entity

        if not self.entity:
            raise ValueError

        self.fill_args()
        return search.filter(self.filter_type, **self._kwargs)

class TermsFilter(Filter):
    """
    Filter for terms
    """
    filter_type = 'terms'

    def fill_args(self):
        self._kwargs[self.get_field_name()] = [self.field_value]


class GreaterThan(Filter):
    """
    Filter for ranges greater than
    """
    filter_type = 'range'

    def fill_args(self):
        self._kwargs[self.get_field_name()] = {'gt': self.field_value}
