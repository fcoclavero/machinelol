# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-07-29 00:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recomendation', '0002_auto_20160721_1929'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lasuser',
            name='registrationDate',
            field=models.DateTimeField(blank=True, null=True, verbose_name='registration date'),
        ),
    ]