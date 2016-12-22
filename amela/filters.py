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

    def __init__(self, filter_type, field_name, field_value):
        self.__type = filter_type
        self.__field_name = field_name
        self.__field_value = field_value

    def type(self):
        return self.__type

    def field_name(self):
        return self.__field_name

    def field_value(self):
        return self.__field_value


class Terms(Filter):
    """
    Filter for terms
    """

    def __init__(self, field_name, field_value):
        super().__init__('terms', field_name, field_value)


class Range(Filter):
    """
    Filter for ranges
    """

    def __init__(self, field_name, field_value):
        super().__init__('range', field_name, field_value)


class GreaterThan(Range):
    """
    Filter for ranges greater than
    """

    def __init__(self, field_name, n):
        super().__init__(field_name, field_value={'gt': n})
