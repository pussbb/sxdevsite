# -*- coding: utf-8 -*-
"""

"""

from django.contrib import admin

# Register your models here.
from .models import Locales, Applications, Translations


class LocaleAdmin(admin.ModelAdmin):
    list_display = ('name', 'locale')
    search_fields = ('name', 'locale')


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'abbreviation')
    search_fields = ('name', 'abbreviation')


class TranslationsAdmin(admin.ModelAdmin):
    list_display = ('locale', 'application', 'author_details')
    search_fields = ('local', 'application')

    def author_details(self, instance):
        return '{0} ({1})'.format(
            instance.author.get_full_name(),
            instance.author.email
        )


admin.site.register(Locales, LocaleAdmin)
admin.site.register(Applications, ApplicationAdmin)
admin.site.register(Translations, TranslationsAdmin)