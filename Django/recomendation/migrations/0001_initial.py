# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-23 18:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('player_id', models.IntegerField()),
            ],
        ),
    ]
