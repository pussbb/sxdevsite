# -*- coding: utf-8 -*-
"""

"""
from django import forms
# our new form
from django.core.mail import mail_admins


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
