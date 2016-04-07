# -*- coding: utf-8 -*-
"""sxdevsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.views.generic import RedirectView

from sxdevsite import settings
from . import views


urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/tr')),
    url(r'^tr/', include('sxtr.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^account/login', views.user_login),
    url(r'^account/logout', views.user_logout),
    url(r'^account/profile', views.user_profile),
    url(r'^account/register', views.user_register),
    url(r'^account/reset', views.user_reset),
    url(r'^account/change_password', views.user_change_pswd),
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/favicon.ico')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
