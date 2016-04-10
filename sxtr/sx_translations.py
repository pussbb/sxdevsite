# -*- coding: utf-8 -*-
"""

"""
import os

from . import TEMPLATE_TR_FILES_DIR

SAC_TR_FILE = os.path.join(TEMPLATE_TR_FILES_DIR, 'Strings.js')

class SxTr(object):

    def __init__(self):
        self._origin = {}
        self._tr = {}

    def __iter__(self):
        yield from self.__next__

    def __next__(self):
        yield from self.items()

    def items(self):
        for key, value in self._origin.items():
            yield key, {'tr': self._tr.get(key), 'origin': value}


class SacTr(SxTr):

    def __init__(self, tr_data):
        self._origin = self._parse(open(SAC_TR_FILE))
        self._tr = self._parse(tr_data)

    def _parse(self, data):
        result = {}
        for line in data:
            if not line.startswith('UIstrings.'):
                continue
            key, value = [i.strip(' ";') for i in line.split(' =', 1)]
            key = key.split('.')[-1]
            value = value.strip("\";\n")
            if value == 'null':
                value = None
            if key.endswith(']'):
                key = '.'.join(i.strip('[]"') for i in key.split('['))
            result[key] = value
        return result


"""
sac_tr = SacTr(open(os.path.join(TEMPLATE_TR_FILES_DIR, 'Strings_de.js')))
for key, value in sac_tr.items():
    print(key, value)
"""