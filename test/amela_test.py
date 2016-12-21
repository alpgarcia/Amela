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

import amela.filters.terms_filter
import amela.metric

# Test script on how to build metrics with Amela module

if __name__ == '__main__':
    # Search for messages that contain 'merge'
    tf = amela.filters.terms_filter.TermFilter('message_analyzed', 'merge')
    metric_result = amela.metric.Metric(["http://127.0.0.1:9200"], 'git').filter(tf).execute()
    print(metric_result.to_dict())

    # COUNTING UNIQUE COMMITS AND IGNORING 'MERGES'
    #s = Search(using=client, index="git").filter('range', files={'gt':0})

    #s.aggs.metric('commits', 'cardinality', field='hash')
    #result = s.execute()
    #result.to_dict()["aggregations"]
