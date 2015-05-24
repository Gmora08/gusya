# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_email', '0002_auto_20150520_0654'),
    ]

    operations = [
        migrations.AddField(
            model_name='waitinglist',
            name='active_user',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='waitinglist',
            name='phone_number',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
