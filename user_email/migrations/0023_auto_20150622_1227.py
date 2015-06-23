# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_email', '0022_remove_payment_operation_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='waitinglist',
            name='email',
            field=models.EmailField(max_length=254, unique=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='waitinglist',
            name='phone_number',
            field=models.BigIntegerField(default=0, verbose_name=b'Numero Telefonico'),
            preserve_default=False,
        ),
    ]
