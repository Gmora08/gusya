# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_email', '0009_auto_20150526_1337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='waitinglist',
            name='activation_date',
            field=models.DateTimeField(null=True, editable=False),
        ),
    ]
