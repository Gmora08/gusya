# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_email', '0012_waitinglist_token_client'),
    ]

    operations = [
        migrations.AlterField(
            model_name='waitinglist',
            name='token_card',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='waitinglist',
            name='token_client',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
    ]
