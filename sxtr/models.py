# -*- coding: utf-8 -*-
"""

"""
from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Locales(models.Model):

    name = models.CharField(max_length=250)
    locale = models.CharField(max_length=200)

    class Meta:
        unique_together = ('name', 'locale')


class Applications(models.Model):
    name = models.CharField(max_length=250)
    abbreviation = models.CharField(max_length=250)


class Translations(models.Model):
    locale = models.ForeignKey(Locales)
    application = models.ForeignKey(Applications)
    translation = models.TextField()
    author = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        permissions = (
            ('edit_tr', 'Edit Translation'),
        )