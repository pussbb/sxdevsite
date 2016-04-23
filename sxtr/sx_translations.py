# -*- coding: utf-8 -*-
"""

"""
import os
from collections import OrderedDict
import xml.etree.ElementTree as ET

import io
from zipfile import ZipFile

from . import TEMPLATE_TR_FILES_DIR

SAC_TR_FILE = os.path.join(TEMPLATE_TR_FILES_DIR, 'Strings.js')
SWA_TR_FILE = os.path.join(TEMPLATE_TR_FILES_DIR, 'strings.xml')


class SxTr(object):

    content_type = 'text/plain'

    def __init__(self, model):
        self._model = model
        self._origin = self._parse(self._origin_document())
        self._tr = self._parse(None, self._origin.fromkeys(self._origin.keys()))

    def _origin_document(self):
        raise NotImplementedError

    def _parse(self):
        raise NotImplementedError

    def to_string(self):
        raise NotImplementedError

    def filename(self):
        raise NotImplementedError

    def to_json(self):
        for key, value in self._origin.items():
            yield {'key': key, 'tr': self._tr.get(key), 'origin': value}

    def update(self, data: dict):
        self._tr.update(data)

    def __repr__(self):
        return self.to_string()

    def as_file(self):
        return self.to_string()


class SacTr(SxTr):

    content_type = 'application/javascript'

    def _origin_document(self):
        yield from open(SAC_TR_FILE)

    def _parse(self, data, result=None):
        if not result:
            result = OrderedDict()
        if not data:
            data = self._model.translation.split("\n")

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

    def filename(self):
        return 'Strings_{}.js'.format(self._model.locale.locale.split('_')[-1])


class SwaTr(SxTr):

    content_type = 'application/octet-stream'

    def to_string(self):
        xml = ET.parse(self._origin_document())
        root = xml.getroot()
        for key, value in self._tr.items():
            if not value:
                value = ''
            for elem in root.findall('./string[@id="{0}"]'.format(key)):
                elem.text = value
        result = io.BytesIO()
        xml.write(result, encoding="utf-8", method="xml", xml_declaration=True)
        return result.getvalue().decode('utf-8')

    def filename(self):
        return 'swa_{}.zip'.format(self._model.locale.locale)

    def as_file(self):
        buf = io.BytesIO()
        tmp_zip = ZipFile(buf, 'w')
        tmp_zip.writestr(
            '{0}/strings.xml'.format(self._model.locale.locale),
            self.to_string()
        )
        tmp_zip.close()
        buf.seek(0)
        return buf

    def _parse(self, data, result=None):
        if not result:
            result = OrderedDict()

        if not data:
            if not self._model.translation:
                return result
            xml = ET.fromstring(self._model.translation)
        else:
            xml = ET.parse(data).getroot()

        for elem in xml:
            result[elem.attrib.get('id')] = ''.join(elem.itertext())
        return result

    def _origin_document(self):
        return open(SWA_TR_FILE)
