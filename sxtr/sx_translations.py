# -*- coding: utf-8 -*-
"""

"""
import os
from collections import OrderedDict
from copy import deepcopy

from . import TEMPLATE_TR_FILES_DIR

SAC_TR_FILE = os.path.join(TEMPLATE_TR_FILES_DIR, 'Strings.js')

class SxTr(object):

    def __init__(self):
        if not self._tr:
            self._tr = self._tr.fromkeys(self._origin.keys())

    def to_json(self):
        for key, value in self._origin.items():
            yield {'key': key, 'tr': self._tr.get(key), 'origin': value}

    def to_string(self):
        raise NotImplemented

    def update(self, data: dict):
        self._tr.update(data)

    def __repr__(self):
        return self.to_string()


class SacTr(SxTr):

    def __init__(self, tr_data):
        self._origin = self._parse(open(SAC_TR_FILE))
        self._tr = self._parse(
            tr_data.split("\n"),
            self._origin.fromkeys(self._origin.keys())
        )
        super().__init__()

    def _parse(self, data, default=None):
        if not default:
            default = OrderedDict()
        result = default
        for line in data:
            if not line.startswith('UIstrings.'):
                continue
            key, value = self.__parse_line(line)
            if not value or value.startswith('UIstrings.') or value == '.':
                continue
            if 'regexp' in key.lower() or 'convertCharacter' in key:
                continue
            result[key] = value
        return result

    def __parse_line(self, line):
        key, value = [i.strip(' ";') for i in line.split(' =', 1)]
        key = key.split('.')[-1]
        value = value.strip("\";\n")
        if value == 'null':
            value = None
        if key.endswith(']'):
            key = '.'.join(i.strip('[]"') for i in key.split('['))
        return key, value

    def to_string(self):
        result = []
        for line in open(SAC_TR_FILE):
            if not line.startswith('UIstrings.'):
                result.append(line)
                continue
            key, _ = self.__parse_line(line)
            if key not in self._tr:
                result.append(line)
                continue
            parts = line.split(' =')
            value = self._tr.get(key)
            if not value:
                value = ''
            parts[-1] = '"{0}"'.format(value)
            result.append(' = '.join(parts))
        return "\n".join(result)