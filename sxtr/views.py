# -*- coding: utf-8 -*-
"""

"""
from django.http import HttpResponse
from django.shortcuts import render

from django.http import JsonResponse
from django.views.generic.edit import FormView

from sxdevsite.request.utils import get_post_data
from sxtr.apps import SxTrConfig
from .forms import ContactForm
#from django.contrib.auth.mixins import LoginRequiredMixin


JS_APP_FILES = [
    'sxtr/application.js',
    'sxtr/directives/directives.js',
    'sxtr/controllers/AboutController.js',
    'sxtr/controllers/ContactController.js',
    'sxtr/controllers/AccessDeniedController.js',
    'sxtr/controllers/MainController.js',
    'sxtr/controllers/AuthControllers.js',
    'sxtr/services/AuthInterceptor.js',
    'sxtr/route.js',
    'sxtr/services/Session.js',
    'sxtr/services/Requests.js',
]


def index(request):
    context = {
        'project_title': SxTrConfig.name,
        'JS_APP_FILES': JS_APP_FILES
    }
    return HttpResponse(render(request, 'index.html', context))


class JsonRequestForm(FormView):

    def get_form_kwargs(self):
        data = super().get_form_kwargs()
        data['data'] = get_post_data(self.request)
        return data

    def form_invalid(self, form):
        return JsonResponse({'errors': form.errors}, status=400)

    def form_valid(self, form):
        return HttpResponse(status=204)


class ContactView(JsonRequestForm):

    form_class = ContactForm

    def form_valid(self, form):
        form.send_email()
        return super().form_valid(form)
