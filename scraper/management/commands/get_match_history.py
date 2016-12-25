import dota2api
import json

from django.core.management.base import BaseCommand
from scraper.models import *

class Command(BaseCommand):
    help = 'get latest N * 100 matches basic info'

    def add_arguments(self, parser):
        parser.add_argument('n', nargs='?', type=int)

    def handle(self, *args, **options):
        # init api client
        self.api = dota2api.Initialise()

        if not self.api:
            return False

        # continue with next_execution
        for i in range(options['n']):
            self.fetch_next()

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
        for data in res['matches']:
            self.dump_match(data)
        return e


    def dump_player(self, data):
        if 'account_id' not in data:
            return None
        p = Player.objects.get_or_create(account_id = data['account_id'])
        return p[0]

    def dump_hero(self, data):
        h = Hero.objects.get_or_create(hero_id = data['hero_id'])
        return h[0]

    def dump_match_player(self, match, data):
        try:
            player = self.dump_player(data)
            mp, c = MatchPlayer.objects.get_or_create(
                    match = match, player = player)
            if c:
                mp.hero = self.dump_hero(data)
                mp.player_slot = int(data.get('player_slot', 0))
                mp.assists = int(data.get('assists', 0))
                mp.backpack_0 = int(data.get('backpack_0', 0))
                mp.backpack_1 = int(data.get('backpack_1', 0))
                mp.backpack_2 = int(data.get('backpack_2', 0))
                mp.deaths = int(data.get('deaths', 0))
                mp.denies = int(data.get('denies', 0))
                mp.gold = int(data.get('gold', 0))
                mp.gold_per_min = int(data.get('gold_per_min', 0))
                mp.gold_spent = int(data.get('gold_spent', 0))
                mp.hero_damage = int(data.get('hero_damage', 0))
                mp.hero_healing = int(data.get('hero_healing', 0))
                mp.item_0 = int(data.get('item_0', 0))
                mp.item_1 = int(data.get('item_1', 0))
                mp.item_2 = int(data.get('item_2', 0))
                mp.item_3 = int(data.get('item_3', 0))
                mp.item_4 = int(data.get('item_4', 0))
                mp.item_5 = int(data.get('item_5', 0))
                mp.kills = int(data.get('kills', 0))
                mp.last_hits = int(data.get('last_hits', 0))
                mp.leaver_status = int(data.get('leaver_status', 0))
                mp.level = int(data.get('level', 0))
                mp.scaled_hero_damage = int(data.get('scaled_hero_damage', 0))
                mp.scaled_hero_healing = int(data.get('scaled_hero_healing', 0))
                mp.scaled_tower_damage = int(data.get('scaled_tower_damage', 0))
                mp.tower_damage = int(data.get('tower_damage', 0))
                mp.xp_per_min = int(data.get('xp_per_min', 0))
                mp.save()
            return mp
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

            for i in data['players']:
                self.dump_match_player(m, i)
        return m

    def dump_execution(self, res, start_at_match_seq_num = 0):
        e = Execution()
        e.start_at_match_seq_num = start_at_match_seq_num
        e.raw_response = json.dumps(res)
        e.save()

        match_seq_num = [x['match_seq_num'] for x in res['matches']]
        if match_seq_num:
            e.next_start_at_match_seq_num = max(match_seq_num)

        if Match.objects.filter(match_seq_num__in = match_seq_num).exists():
            e.next_execution = e

        e.save()

        self.puts('start_at: %d' % e.start_at_match_seq_num)
        self.puts('next: %d' % e.next_start_at_match_seq_num)

        return e

    def puts(self, message, ending = None):
        self.stdout.write(message, ending)

