# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('user_email', '0005_auto_20150523_1314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='waitinglist',
            name='key_expires',
            field=models.DateTimeField(default=datetime.date(2015, 5, 25), null=True, blank=True),
        ),
    ]
