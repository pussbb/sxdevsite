# -*- coding: utf-8 -*-
"""

"""
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from sxtr.sx_translations import SacTr


class Locales(models.Model):

    name = models.CharField(max_length=250)
    locale = models.CharField(max_length=200)

    class Meta:
        unique_together = ('name', 'locale')
        ordering = ('locale',)


class Applications(models.Model):
    name = models.CharField(max_length=250)
    abbreviation = models.CharField(max_length=250)

    class Meta:
        ordering = ('name',)

    def lexer(self):
        if self.abbreviation == 'sac':
            return SacTr
        elif self.abbreviation == 'swa':
            pass
        raise Exception('Application not supported')


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
        unique_together = ('application', 'locale')

    def grammar(self):
        return self.application.lexer()(self)

