# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_email', '0013_auto_20150601_1342'),
    ]

    operations = [
        migrations.AddField(
            model_name='waitinglist',
            name='card_number',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
