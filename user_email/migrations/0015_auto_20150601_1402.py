# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_email', '0014_waitinglist_card_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='waitinglist',
            name='card_number',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
