# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_email', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='waitinglist',
            name='email',
            field=models.EmailField(unique=True, max_length=254),
        ),
        migrations.AlterField(
            model_name='waitinglist',
            name='referenced_users',
            field=models.IntegerField(default=0, null=True, blank=True),
        ),
    ]
