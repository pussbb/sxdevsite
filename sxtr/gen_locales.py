# -*- coding: utf-8 -*-
"""

"""
import os
import json

from icu import Locale

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

locales = []
for locale in Locale.getAvailableLocales().values():
    locales.append({'locale': locale.getName(),
                    'name': locale.getDisplayName(locale)})

json.dump(locales, open(os.path.join(BASE_PATH, 'locales.json'), 'w'))