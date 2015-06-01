# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('user_email', '0010_auto_20150526_1733'),
    ]

    operations = [
        migrations.AddField(
            model_name='waitinglist',
            name='token_card',
            field=models.CharField(max_length=500, null=True, editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='waitinglist',
            name='key_expires',
            field=models.DateTimeField(default=datetime.date(2015, 6, 1), null=True, blank=True),
        ),
    ]
