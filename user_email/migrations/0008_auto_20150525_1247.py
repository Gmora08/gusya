# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_email', '0007_auto_20150525_1244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='waitinglist',
            name='last_name',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Apellido', blank=True),
        ),
        migrations.AlterField(
            model_name='waitinglist',
            name='name',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Nombre', blank=True),
        ),
        migrations.AlterField(
            model_name='waitinglist',
            name='phone_number',
            field=models.BigIntegerField(null=True, verbose_name=b'Numero Telefonico', blank=True),
        ),
    ]
