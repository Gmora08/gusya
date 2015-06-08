# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_email', '0018_auto_20150604_0045'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='waitinglist',
            name='key_expires',
        ),
        migrations.RemoveField(
            model_name='waitinglist',
            name='reference_code',
        ),
        migrations.AddField(
            model_name='waitinglist',
            name='mail_sent',
            field=models.BooleanField(default=False),
        ),
    ]
