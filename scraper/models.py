from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Execution(models.Model):
    start_at_match_seq_num = models.BigIntegerField(default = 0)

    next_start_at_match_seq_num = models.BigIntegerField(default = 0)
    next_execution = models.ForeignKey('Execution', null = True)

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)


class Match(models.Model):
    match_id = models.BigIntegerField(primary_key = True, default = 0)

    match_seq_num = models.BigIntegerField(default = 0, unique = True)
    start_time = models.IntegerField(default = 0)
    lobby_type = models.IntegerField(default=0)

    barracks_status_dire = models.IntegerField(default=0)
    barracks_status_radiant = models.IntegerField(default=0)
    cluster = models.IntegerField(default=0)
    dire_score = models.IntegerField(default=0)
    duration = models.IntegerField(default=0)
    engine = models.IntegerField(default=1)
    first_blood_time = models.IntegerField(default=0)
    flags = models.IntegerField(default=0)
    game_mode = models.IntegerField(default=0)
    human_players = models.IntegerField(default=0)
    leagueid = models.BigIntegerField(default=0)
    negative_votes = models.IntegerField(default=0)
    positive_votes = models.IntegerField(default=0)
    radiant_score = models.IntegerField(default=0)
    radiant_win = models.BooleanField(default=True)
    season = models.IntegerField(null=True)
    tower_status_dire = models.IntegerField(default=0)
    tower_status_radiant = models.IntegerField(default=0)

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
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, null=True)
    hero = models.ForeignKey(Hero, null=True)

    # ability_upgrades
    assists = models.IntegerField(default = 0)
    backpack_0 = models.IntegerField(default = 0)
    backpack_1 = models.IntegerField(default = 0)
    backpack_2 = models.IntegerField(default = 0)
    deaths = models.IntegerField(default = 0)
    denies = models.IntegerField(default = 0)
    gold = models.IntegerField(default = 0)
    gold_per_min = models.IntegerField(default = 0)
    gold_spent = models.IntegerField(default = 0)
    hero_damage = models.IntegerField(default = 0)
    hero_healing = models.IntegerField(default = 0)
    item_0 = models.IntegerField(default = 0)
    item_1 = models.IntegerField(default = 0)
    item_2 = models.IntegerField(default = 0)
    item_3 = models.IntegerField(default = 0)
    item_4 = models.IntegerField(default = 0)
    item_5 = models.IntegerField(default = 0)
    kills = models.IntegerField(default = 0)
    last_hits = models.IntegerField(default = 0)
    leaver_status = models.IntegerField(default = 0)
    level = models.IntegerField(default = 0)
    scaled_hero_damage = models.IntegerField(default = 0)
    scaled_hero_healing = models.IntegerField(default = 0)
    scaled_tower_damage = models.IntegerField(default = 0)
    tower_damage = models.IntegerField(default = 0)
    xp_per_min = models.IntegerField(default = 0)

    player_slot = models.IntegerField(default = 0)


class AbilityUpgrade(models.Model):
    match_player = models.ForeignKey(MatchPlayer, on_delete=models.CASCADE)

    level = models.IntegerField(default = 0)
    ability = models.IntegerField(default = 0)
    time = models.IntegerField(default = 0)

