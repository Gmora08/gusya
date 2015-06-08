# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_email', '0019_auto_20150608_0845'),
    ]

    operations = [
        migrations.AddField(
            model_name='waitinglist',
            name='invitation_url',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
