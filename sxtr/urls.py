# -*- coding: utf-8 -*-
"""

"""
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^contact/', views.ContactView.as_view(), name='contact'),
    url(r'^translations/(?:(?P<locale_id>\d+))?$', views.TranslationView.as_view(),),
    url(r'^locales/$', views.locales_list),
    url(r'^apps/$', views.apps_list),
]
