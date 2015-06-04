# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('user_email', '0016_auto_20150602_1336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='currency',
            field=models.CharField(max_length=4, choices=[(b'MXN', b'MXN'), (b'USD', b'USD')]),
        ),
        migrations.AlterField(
            model_name='waitinglist',
            name='key_expires',
            field=models.DateTimeField(default=datetime.date(2015, 6, 3), null=True, blank=True),
        ),
    ]
