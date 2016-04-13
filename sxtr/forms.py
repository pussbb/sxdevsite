# -*- coding: utf-8 -*-
"""

"""
from django import forms
# our new form
from django.core.mail import mail_admins
from django.forms import ModelForm

from sxtr.models import Translations


class ContactForm(forms.Form):

    name = forms.CharField(required=True, initial='')
    email = forms.EmailField(required=True, initial='')
    message = forms.CharField(
        required=True,
        widget=forms.Textarea,
        initial=''
    )

    def send_email(self):
        subject = self.cleaned_data['name'] + ' ' + self.cleaned_data['email']
        message = self.cleaned_data['message']
        mail_admins(subject, message)


class TranslationForm(ModelForm):
    class Meta:
        model = Translations
        fields = ('locale', 'application')