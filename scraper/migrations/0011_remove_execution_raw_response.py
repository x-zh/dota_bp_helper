# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-26 20:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0010_abilityupgrade'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='execution',
            name='raw_response',
        ),
    ]
