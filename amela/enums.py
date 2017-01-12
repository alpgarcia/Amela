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
#   Alberto Pérez García-Plaza <alpgarcia@bitergia.com>
#   Daniel Izquierdo Cortazar <dizquierdo@bitergia.com>
#

from enum import Enum, unique

@unique
class Interval(Enum):
    year    = 1
    quarter = 2
    month   = 3
    week    = 4
    day     = 5
    hour    = 6
    minute  = 7
    second  = 8

#
# @unique
# class MetricType(Enum):
#     avg = 0
#     median = 1
#     count = 2
#     unique_count = 3
#     max_value = 4
#     min_value = 5
#     sum_values = 6
#
# @unique
# class BucketType(Enum):
#     terms = 0
#     date = 1
