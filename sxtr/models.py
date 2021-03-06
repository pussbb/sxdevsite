# -*- coding: utf-8 -*-
"""

"""
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from sxtr.sx_translations import SacTr, SwaTr


class Locales(models.Model):

    name = models.CharField(max_length=250)
    locale = models.CharField(max_length=200)

    class Meta:
        unique_together = ('name', 'locale')
        ordering = ('locale',)
        verbose_name = 'locale'
        verbose_name_plural = 'locales'

    def __str__(self):
        return '{0} ({1})'.format(self.name, self.locale)

    def __unicode__(self):
        return self.__str__().encode('utf-8')


class Applications(models.Model):
    name = models.CharField(max_length=250)
    abbreviation = models.CharField(max_length=250)

    class Meta:
        ordering = ('name',)
        unique_together = ('name', 'abbreviation')
        verbose_name = 'application'
        verbose_name_plural = 'applications'

    def lexer(self):
        if self.abbreviation == 'sac':
            return SacTr
        elif self.abbreviation == 'swa':
            return SwaTr
        raise NotImplementedError('Application not supported')

    def __str__(self):
        return '{0} ({1})'.format(self.name, self.abbreviation)

    def __unicode__(self):
        return self.__str__().encode('utf-8')


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

        verbose_name = 'translation'
        verbose_name_plural = 'translations'

    def grammar(self):
        return self.application.lexer()(self)

