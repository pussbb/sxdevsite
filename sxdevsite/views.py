# -*- coding: utf-8 -*-
"""

"""

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, \
    UserCreationForm, PasswordResetForm, PasswordChangeForm

from django.forms import model_to_dict
from django.http import HttpResponseNotAllowed, JsonResponse, HttpResponse


from sxdevsite.request.utils import get_post_data


def user_login(request):
    if request.method != 'POST' or request.user.is_authenticated():
        return HttpResponseNotAllowed(['POST'])
    auth_form = AuthenticationForm(None, get_post_data(request))
    if auth_form.is_valid():
        login(request, auth_form.get_user())
        return user_details(request)
    return JsonResponse({'errors': auth_form.errors}, status=400)


@login_required
def user_logout(request):
    logout(request)
    return HttpResponse(status=204)


class UpdateProfileForm(UserChangeForm):

    class Meta(UserChangeForm.Meta):
        fields = ('first_name', 'last_name', 'email', 'password')


@login_required
def user_profile(request):
    if request.method == 'POST':
        form = UpdateProfileForm(get_post_data(request), instance=request.user)
        if not form.is_valid():
            JsonResponse({'errors': form.errors}, status=400)
        request.user = form.save()
    return user_details(request)


def user_details(request):
    return JsonResponse(
        model_to_dict(request.user, exclude=['password']),
        safe=False
    )


def user_register(request):
    if request.method != 'POST' or request.user.is_authenticated():
        return HttpResponseNotAllowed(['POST'])

    form = UserCreationForm(get_post_data(request))
    if not form.is_valid():
        return JsonResponse({'errors': form.errors}, status=400)

    return JsonResponse(
        model_to_dict(form.save(), exclude=['password']),
        safe=False
    )


def user_reset(request):
    if request.method != 'POST' or request.user.is_authenticated():
        return HttpResponseNotAllowed(['POST'])

    form = PasswordResetForm(get_post_data(request))
    if not form.is_valid():
        return JsonResponse({'errors': form.errors}, status=400)
    form.save()
    return HttpResponse(status=204)


@login_required
def user_change_pswd(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    form = PasswordChangeForm(request.user, get_post_data(request))
    if not form.is_valid():
        return JsonResponse({'errors': form.errors}, status=400)
    form.save()
    return HttpResponse(status=204)
