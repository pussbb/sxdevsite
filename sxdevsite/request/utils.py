# -*- coding: utf-8 -*-
"""

"""

import json


def get_post_data(request):
    data = request.POST.dict()
    if 'application/json' in request.META.get('CONTENT_TYPE', ''):
        data.update(json.loads(request.body.decode('utf-8')))
    return data
