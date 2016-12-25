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
        player = self.dump_player(data)
        mp, c = MatchPlayer.objects.get_or_create(
                match = match, player = player)
        if c:
            mp.hero = self.dump_hero(data)
            mp.player_slot = data['player_slot']
            mp.save()
        return mp

    def dump_match(self, data):
        m, c = Match.objects.get_or_create(match_id = data['match_id'])
        if c:
            m.match_seq_num = data['match_seq_num']
            m.start_time = data['start_time']
            m.lobby_type = int(data['lobby_type'])
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

