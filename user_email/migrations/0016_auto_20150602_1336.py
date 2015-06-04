# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('user_email', '0015_auto_20150601_1402'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mount', models.FloatField()),
                ('description', models.CharField(max_length=400)),
                ('status', models.BooleanField(default=False)),
                ('currency', models.CharField(max_length=4)),
                ('order_id', models.CharField(max_length=100)),
                ('creation_date', models.DateTimeField(null=True, blank=True)),
                ('operation_date', models.DateTimeField(null=True, blank=True)),
            ],
        ),
        migrations.AlterField(
            model_name='waitinglist',
            name='key_expires',
            field=models.DateTimeField(default=datetime.date(2015, 6, 2), null=True, blank=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='card',
            field=models.ForeignKey(to='user_email.WaitingList'),
        ),
    ]
