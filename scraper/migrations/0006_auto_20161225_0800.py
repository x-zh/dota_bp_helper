# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-25 08:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0005_auto_20161225_0756'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matchplayer',
            name='player',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='scraper.Player'),
        ),
    ]
