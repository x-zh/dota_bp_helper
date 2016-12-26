import dota2api
import json
import time
from datetime import datetime
from django.core.management.base import BaseCommand
from scraper.models import *

class Command(BaseCommand):
    help = 'get latest N * 100 matches basic info'

    def add_arguments(self, parser):
        parser.add_argument('n', nargs='?', type=int)

    def handle(self, *args, **options):
        # init api client
        self.api = dota2api.Initialise()

        # in-mem caches
        self.heros = {}
        self.players = {}

        if not self.api:
            return False

        # continue with next_execution
        for i in range(options['n']):
            start_time = datetime.now()
            self.fetch_next()
            end_time = datetime.now()
            time_diff = (end_time - start_time).seconds
            # time.sleep(time_diff)
            self.puts(self.style.SUCCESS(
                '%d00 matches in %d seconds' % (i + 1, time_diff)))

        self.puts(self.style.SUCCESS('Done'))

    def fetch_next(self):
        # what's next
        prev_e = Execution.objects \
                .filter(next_execution__isnull = True) \
                .exclude(next_start_at_match_seq_num = 0) \
                .order_by('-next_start_at_match_seq_num') \
                .first()

        if prev_e:
            start_at_match_seq_num = prev_e.next_start_at_match_seq_num + 1
            res = self.api.get_match_history_by_seq_num(
                    start_at_match_seq_num = start_at_match_seq_num)
            e = self.dump(res, start_at_match_seq_num)
            prev_e.next_execution = e
            prev_e.save()
            return e
        else:
            res = self.api.get_match_history_by_seq_num(
                    start_at_match_seq_num = 2500000000)
            e = self.dump(res, 2500000000)
            return e

    def dump(self, res, start_at_match_seq_num = 0):
        e = self.dump_execution(res, start_at_match_seq_num)

        self.dump_players(res['matches'])
        self.dump_heros(res['matches'])

        for data in res['matches']:
            self.dump_match(data)

        return e

    def dump_players(self, data):
        account_ids = set()
        for i in data:
            account_ids |= set([x.get('account_id') for x in i['players']])
        account_ids -= set([None,])

        ps = Player.objects.filter(account_id__in = account_ids)

        # players already in db
        for p in ps:
            self.players[p.account_id] = p

        # players not in db
        new_account_ids = account_ids - set(self.players.keys())
        ps = []
        for i in new_account_ids:
            p = Player(account_id = i)
            ps.append(p)
        Player.objects.bulk_create(ps)
        for p in ps:
            self.players[p.account_id] = p

        return self.players

    def dump_heros(self, data):
        hero_ids = set()
        for i in data:
            hero_ids |= set([x.get('hero_id') for x in i['players']])
        hero_ids -= set([None,])

        hs = Hero.objects.filter(hero_id__in = hero_ids)

        # heros already in db
        for h in hs:
            self.heros[h.hero_id] = h

        # heros not in db
        new_hero_ids = hero_ids - set(self.heros.keys())
        hs = []
        for i in new_hero_ids:
            h = Hero(hero_id = i)
            hs.append(h)
        Hero.objects.bulk_create(hs)
        for h in hs:
            self.heros[h.hero_id] = h

        return self.heros

    def create_match_player(self, match, data):
        try:
            player = None
            if 'account_id' in data and data['account_id'] in self.players:
                player = self.players[data['account_id']]
            hero = None
            if 'hero_id' in data and data['hero_id'] in self.players:
                hero = self.heros[data['hero_id']]

            mp = MatchPlayer(
                    match=match,
                    player=player,
                    hero = hero,
                    player_slot = int(data.get('player_slot', 0)),
                    assists = int(data.get('assists', 0)),
                    backpack_0 = int(data.get('backpack_0', 0)),
                    backpack_1 = int(data.get('backpack_1', 0)),
                    backpack_2 = int(data.get('backpack_2', 0)),
                    deaths = int(data.get('deaths', 0)),
                    denies = int(data.get('denies', 0)),
                    gold = int(data.get('gold', 0)),
                    gold_per_min = int(data.get('gold_per_min', 0)),
                    gold_spent = int(data.get('gold_spent', 0)),
                    hero_damage = int(data.get('hero_damage', 0)),
                    hero_healing = int(data.get('hero_healing', 0)),
                    item_0 = int(data.get('item_0', 0)),
                    item_1 = int(data.get('item_1', 0)),
                    item_2 = int(data.get('item_2', 0)),
                    item_3 = int(data.get('item_3', 0)),
                    item_4 = int(data.get('item_4', 0)),
                    item_5 = int(data.get('item_5', 0)),
                    kills = int(data.get('kills', 0)),
                    last_hits = int(data.get('last_hits', 0)),
                    leaver_status = int(data.get('leaver_status', 0)),
                    level = int(data.get('level', 0)),
                    scaled_hero_damage = int(data.get('scaled_hero_damage', 0)),
                    scaled_hero_healing = int(data.get('scaled_hero_healing', 0)),
                    scaled_tower_damage = int(data.get('scaled_tower_damage', 0)),
                    tower_damage = int(data.get('tower_damage', 0)),
                    xp_per_min = int(data.get('xp_per_min', 0)))
            mp.save()
            aus = []
            if 'ability_upgrades' in data:
                for au_data in data['ability_upgrades']:
                    au = AbilityUpgrade(
                            level = int(au_data.get('level', 0)),
                            ability = int(au_data.get('ability', 0)),
                            time = int(au_data.get('time', 0)),
                            match_player=mp)
                    aus.append(au)

            return mp, aus
        except:
            self.puts(self.style.ERROR(data))
            raise

    def dump_match(self, data):
        m, c = Match.objects.get_or_create(match_id = data['match_id'])

        if c:
            m.match_seq_num = data['match_seq_num']
            m.start_time = data['start_time']
            m.lobby_type = int(data.get('lobby_type', 0))

            m.barracks_status_dire = int(data.get('barracks_status_dire', 0))
            m.barracks_status_radiant = int(data.get('barracks_status_radiant', 0))
            m.cluster = int(data.get('cluster', 0))
            m.dire_score = int(data.get('dire_score', 0))
            m.duration = int(data.get('duration', 0))
            m.engine = int(data.get('engine', 0))
            m.first_blood_time = int(data.get('first_blood_time', 0))
            m.flags = int(data.get('flags', 0))
            m.game_mode = int(data.get('game_mode', 0))
            m.human_players = int(data.get('human_players', 0))
            m.leagueid = int(data.get('leagueid', 0))
            m.negative_votes = int(data.get('negative_votes', 0))
            m.positive_votes = int(data.get('positive_votes', 0))
            m.radiant_score = int(data.get('radiant_score', 0))
            m.radiant_win = bool(data.get('radiant_win', 0))
            m.tower_status_dire = int(data.get('tower_status_dire', 0))
            m.tower_status_radiant = int(data.get('tower_status_radiant', 0))

            # seems like a deprecated field?
            if 'season' in data:
                m.season = int(data.get('season', 0))

            m.save()

            all_aus = []
            for i in data['players']:
                mp, aus = self.create_match_player(m, i)
                if mp and aus:
                    all_aus += aus
            AbilityUpgrade.objects.bulk_create(all_aus)

        return m

    def dump_execution(self, res, start_at_match_seq_num = 0):
        e = Execution()
        e.start_at_match_seq_num = start_at_match_seq_num
        e.save()

        match_seq_num = [x['match_seq_num'] for x in res['matches']]
        if match_seq_num:
            e.next_start_at_match_seq_num = max(match_seq_num)

        if Match.objects.filter(match_seq_num__in = match_seq_num).exists():
            e.next_execution = e

        e.save()
        return e

    def puts(self, message, ending = None):
        self.stdout.write(message, ending = ending)

