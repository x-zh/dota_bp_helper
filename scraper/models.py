from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Execution(models.Model):
    start_at_match_seq_num = models.BigIntegerField(default = 0)
    raw_response = models.TextField()

    next_start_at_match_seq_num = models.BigIntegerField(default = 0)
    next_execution = models.ForeignKey('Execution', null = True)

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)


class Match(models.Model):
    match_id = models.BigIntegerField(primary_key = True, default = 0)

    match_seq_num = models.BigIntegerField(default = 0, unique = True)
    start_time = models.IntegerField(default = 0)
    lobby_type = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)


class Player(models.Model):
    account_id = models.BigIntegerField(primary_key = True)

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)


class Hero(models.Model):
    hero_id = models.IntegerField(primary_key = True, default = 0)

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)


class MatchPlayer(models.Model):
    match = models.ForeignKey(Match)
    player = models.ForeignKey(Player, null=True)
    hero = models.ForeignKey(Hero, null=True)

    player_slot = models.IntegerField(default = 0)

    class Meta:
        unique_together = (('player', 'match'),)

