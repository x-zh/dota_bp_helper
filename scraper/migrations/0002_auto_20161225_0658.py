# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-25 06:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='execution',
            name='next_execution',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='scraper.Execution'),
        ),
        migrations.AddField(
            model_name='execution',
            name='next_start_at_match_id',
            field=models.IntegerField(default=0),
        ),
    ]
