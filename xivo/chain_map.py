# -*- coding: utf-8 -*-

# Copyright (C) 2014 Avencall
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>


# This is a simplified of the ChainMap available in python3.3
class ChainMap(object):

    _not_found = object()

    def __init__(self, *dicts):
        self._dicts = list(dicts)

    def __getitem__(self, key):
        v = self.get(key, self._not_found)
        if v is self._not_found:
            raise KeyError('{key} not found'.format(key=key))

        return v

    def __contains__(self, key):
        return self.get(key, self._not_found) is not self._not_found

    def get(self, key, default=None):
        for d in self._dicts:
            if key in d:
                return d[key]

        return default