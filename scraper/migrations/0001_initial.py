# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-25 06:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Execution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_at_match_id', models.IntegerField(default=0)),
                ('raw_response', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Hero',
            fields=[
                ('hero_id', models.IntegerField(default=0, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('match_id', models.IntegerField(default=0, primary_key=True, serialize=False)),
                ('match_seq_num', models.IntegerField(default=0)),
                ('start_time', models.IntegerField(default=0)),
                ('lobby_type', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='MatchPlayer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player_slot', models.IntegerField(default=0)),
                ('hero', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scraper.Hero')),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scraper.Match')),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('account_id', models.IntegerField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='matchplayer',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scraper.Player'),
        ),
    ]
