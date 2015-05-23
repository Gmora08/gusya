# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_email', '0004_auto_20150523_0939'),
    ]

    operations = [
        migrations.AlterField(
            model_name='waitinglist',
            name='phone_number',
            field=models.BigIntegerField(null=True, blank=True),
        ),
    ]
