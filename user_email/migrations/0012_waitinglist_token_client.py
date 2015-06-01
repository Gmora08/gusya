# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_email', '0011_auto_20150601_1308'),
    ]

    operations = [
        migrations.AddField(
            model_name='waitinglist',
            name='token_client',
            field=models.CharField(max_length=500, null=True, editable=False, blank=True),
        ),
    ]
