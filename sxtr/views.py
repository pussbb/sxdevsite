# -*- coding: utf-8 -*-
"""

"""

from django.contrib.auth.decorators import login_required
from django.forms import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from django.http import JsonResponse, HttpResponseNotFound
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.views.generic.edit import FormView

from sxdevsite.request.utils import get_post_data
from sxtr.apps import SxTrConfig
from sxtr.models import Translations, Locales, Applications
from .forms import ContactForm, TranslationForm

JS_APP_FILES = [
    'sxtr/application.js',
    'sxtr/directives/directives.js',
    'sxtr/controllers/GeneralControllers.js',
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


def dump_models(items):
    return [model_to_dict(item) for item in items]


def locales_list(_):
    return JsonResponse(dump_models(Locales.objects.all()), safe=False)


def apps_list(_):
    return JsonResponse(dump_models(Applications.objects.all()), safe=False)


class TranslationView(View):
    form_class = TranslationForm


    def translation_list(self):
        return [self.dump_tr_model(i, exclude=['translation'])
                for i in Translations.objects.order_by('locale')]

    def dump_tr_model(self, item, exclude=[]):
        result = model_to_dict(item, exclude=exclude)#, exclude=('password',))
        #result['author'] = model_to_dict(item.author, exclude=('password',))
        result['locale'] = model_to_dict(item.locale)
        result['canEdit'] = False
        if self.request.user:
            result['canEdit'] = self.request.user.id == item.author_id
        try:
            result['statistic'] = item.grammar().statistic()
        except NotImplementedError as _:
            pass
        result['application'] = model_to_dict(item.application)
        return result

    def get(self, request, tr_id=None, action=None):
        # JsonResponse(Translations.objects.all(), safe=False)
        # error = [] is not JSON serializable

        if not tr_id:
            return JsonResponse(self.translation_list(), safe=False)

        model = get_object_or_404(Translations, pk=tr_id)
        try:
            translation = model.grammar()
        except NotImplementedError as exp:
            return HttpResponseNotFound(exp)

        #  for now we don't care about any additional action name
        #  the same behaviour for all actions if not None
        if action:
            response = HttpResponse(translation.as_file(),
                                    translation.content_type)
            response['Content-Disposition'] = 'attachment; filename={}'.format(
                translation.filename()
            )
            return response

        result = self.dump_tr_model(model)
        result['translation'] = list(translation.to_json())
        return JsonResponse(result, safe=False)

    @method_decorator(login_required)
    def post(self, request, tr_id=None, action=None):
        if not tr_id:
            return self.__create_new_translation()

        model = get_object_or_404(Translations, pk=tr_id)

        if request.user.id != model.author_id:
            return JsonResponse(
                {'errors': {'__all__': 'You does not have permissions to edit'
                                       ' this record.'}}
                , 400)

        try:
            translation = model.grammar()
        except NotImplementedError as exp:
            return JsonResponse({'errors': {'__all__': str(exp)}}, status=400)

        translation.update(get_post_data(request))
        model.translation = translation.to_string()
        model.save()
        return self.get(request, tr_id)

    def __create_new_translation(self):

        form = TranslationForm(
            get_post_data(self.request),
            instance=Translations(author=self.request.user, translation='')
        )
        if not form.is_valid():
            return JsonResponse({'errors': form.errors}, status=400)

        model = form.save()
        return self.get(self.request, model.id)
