# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_email', '0021_auto_20150611_0236'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='operation_date',
        ),
    ]
