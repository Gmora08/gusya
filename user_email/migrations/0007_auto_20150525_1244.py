# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_email', '0006_auto_20150525_1234'),
    ]

    operations = [
        migrations.AddField(
            model_name='waitinglist',
            name='last_name',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='waitinglist',
            name='name',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
