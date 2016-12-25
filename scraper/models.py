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

    season = models.IntegerField(null=True)
    radiant_win = models.BooleanField(default=True)
    duration = models.IntegerField(default=0)
    tower_status_radiant = models.IntegerField(default=0)
    tower_status_dire = models.IntegerField(default=0)
    barracks_status_radiant = models.IntegerField(default=0)
    barracks_status_dire = models.IntegerField(default=0)
    cluster = models.IntegerField(default=0)
    first_blood_time = models.IntegerField(default=0)
    human_players = models.IntegerField(default=0)
    leagueid = models.BigIntegerField(default=0)
    positive_votes = models.IntegerField(default=0)
    negative_votes = models.IntegerField(default=0)
    game_mode = models.IntegerField(default=0)
    flags = models.IntegerField(default=0)
    engine = models.IntegerField(default=1)
    radiant_score = models.IntegerField(default=0)
    dire_score = models.IntegerField(default=0)

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

