# -*- coding: utf-8 -*-
from django.db import migrations

from django.conf import settings


def init_apps(apps, schema_editor):
    apps_cls = apps.get_model('sxtr', 'Applications')
    apps = [
        {'name': 'swa', 'abbreviation': 'Scalix Webmail Access'},
        {'name': 'sac', 'abbreviation': 'Scalix Administration Access'},
    ]
    for app in apps:
        apps_cls(**app).save()


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sxtr', '0001_initial'),
        ('sxtr', '0002_auto_20160410_0654'),
    ]

    operations = [
        migrations.RunPython(init_apps),
    ]
