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
#   Santiago Dueñas <sduenas@bitergia.com>
#

from amela.query_filters import GreaterThan

class Entity:
    field_name = None
    date_field_name = 'grimoire_creation_date'
    index_name = 'git'

    def __init__(self):
        self.filters = []

class Author(Entity):
    field_name = 'author_name'

# class ClosedIssue(Entity):
#
#     def __init__(self):
#         self._filters.append(ClosedFilter)

class Commit(Entity):
    field_name = 'hash'

    def __init__(self, filter_merges=True):
        super().__init__()
        if filter_merges:
            self.filters.append(GreaterThan(File(), 0))

class Repo(Entity):
    field_name = 'repo_name'

class File(Entity):
    field_name = 'files'

class Project(Entity):
    field_name = 'project'
