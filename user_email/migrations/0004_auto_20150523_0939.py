# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user_email', '0003_auto_20150522_1551'),
    ]

    operations = [
        migrations.AddField(
            model_name='waitinglist',
            name='activation_key',
            field=models.CharField(max_length=40, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='waitinglist',
            name='key_expires',
            field=models.DateTimeField(default=datetime.date(2015, 5, 23), null=True, blank=True),
        ),
        migrations.AddField(
            model_name='waitinglist',
            name='user',
            field=models.OneToOneField(null=True, blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
