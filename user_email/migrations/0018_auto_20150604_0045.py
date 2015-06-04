# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('user_email', '0017_auto_20150603_1646'),
    ]

    operations = [
        migrations.AlterField(
            model_name='waitinglist',
            name='key_expires',
            field=models.DateTimeField(default=datetime.date(2015, 6, 4), null=True, blank=True),
        ),
    ]
