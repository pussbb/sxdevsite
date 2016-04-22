# -*- coding: utf-8 -*-
"""

"""
import os
from collections import OrderedDict
from copy import deepcopy

from . import TEMPLATE_TR_FILES_DIR

SAC_TR_FILE = os.path.join(TEMPLATE_TR_FILES_DIR, 'Strings.js')

class SxTr(object):
    content_type = 'text/plain'

    def __init__(self, tr_data):
        self._origin = self._parse(self._origin_document())
        self._tr = self._parse(
            tr_data,
            self._origin.fromkeys(self._origin.keys())
        )

    def _origin_document(self):
        raise NotImplemented

    def _parse(self):
        raise NotImplemented

    def to_string(self):
        raise NotImplemented

    def to_json(self):
        for key, value in self._origin.items():
            yield {'key': key, 'tr': self._tr.get(key), 'origin': value}

    def update(self, data: dict):
        self._tr.update(data)

    def __repr__(self):
        return self.to_string()


class SacTr(SxTr):

    content_type = 'application/javascript'

    def __init__(self, tr_data):
        super().__init__(tr_data.split("\n"))

    def _origin_document(self):
        yield from open(SAC_TR_FILE)

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
            parts[-1] = '"{0}"'.format(value.replace('"', '\"'))
            result.append(' = '.join(parts))
        return "\n".join(result)