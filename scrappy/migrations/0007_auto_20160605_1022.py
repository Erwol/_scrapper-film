# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-05 10:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrappy', '0006_film_last_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='film',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
