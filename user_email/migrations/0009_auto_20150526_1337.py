# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('user_email', '0008_auto_20150525_1247'),
    ]

    operations = [
        migrations.AddField(
            model_name='waitinglist',
            name='activation_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 26, 18, 37, 5, 338592, tzinfo=utc), editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='waitinglist',
            name='registration_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 26, 18, 37, 25, 798002, tzinfo=utc), editable=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='waitinglist',
            name='key_expires',
            field=models.DateTimeField(default=datetime.date(2015, 5, 26), null=True, blank=True),
        ),
    ]
