#!/usr/bin/env python

import logging
import time
import signal
import sys
from argparse import ArgumentParser
from datetime import datetime, timezone, timedelta
from twitter_stream import StreamClient, BaseStreamEvent, OAuth1, Utils

""" Twitter OAuth
Set your consumer key and access token
"""
twitter_consumer_key        = ''
twitter_consumer_secret     = ''
twitter_access_token        = ''
twitter_access_token_secret = ''

JST_DELTA = timedelta(hours=9)
JST = timezone(JST_DELTA, 'JST')

class StreamEvent(BaseStreamEvent):
    @classmethod
    def _reset_time(klass, now=None):
        if now is None: now = int(time.time())
        return now - now % 60 + 60

    def __init__(self, **options):
        super().__init__()
        self._logger = logging.getLogger(__name__)
        self._count = [0, 0]
        self._count_reset_time = self._reset_time()
        self._parent = None

    # def _set_parent(self, parent):
    #     self._parent = parent
    #     self._default_chunk_size = self._parent.chunk_size()

    def report_count(self, force=False):
        now = int(time.time())
        if force or self._count_reset_time <= now:
            self._logger.info('Index {}, Delete {}'.format(self._count[0], self._count[1]))
            self._count = [0, 0]
            self._count_reset_time = self._reset_time()

    def keep_alive(self):
        self._logger.info('-- keep-alive --')
        self.report_count()

    def nop(self, raw_data):
        self._logger.info('-- nop --')
        self.report_count()

    def on_tweet(self, data):
        self.report_count()
        self._count[0] += 1
        created_at = Utils.parse_created_at(data['created_at'])
        created_at = (created_at + JST_DELTA).replace(tzinfo=JST)
        self._logger.info('{} {}'.format(
            created_at.strftime('%Y-%m-%dT%H:%M:%S'),
            data['text'].replace('\n', ' ')))

    def on_delete(self, data):
        self.report_count()
        self._count[1] += 1
        # self._logger.info('Delete {}'.format(data['delete']['status']['id_str']))

    def on_warning(self, data):
        self.report_count()

def parse_args():
    parser = ArgumentParser()
    parser.add_argument(
        '--debug', dest='debug', default=False, action='store_true')
    parser.add_argument(
        '--compressed', dest='compressed', default=False, action='store_true',
        help='Gzip compressed streaming')
    parser.add_argument(
        '--delimited', dest='delimited', default=False, action='store_true',
        help='Receive tweet length, then tweet data')
    parser.add_argument(
        '--chunk-size', dest='chunk_size', default=1024, type=int,
        help='Read bytes from socket')
    parser.add_argument(
        '--track', dest='track', type=str,
        help='Use filter API with indicated word. If not set, use sample API')
    return parser.parse_args()
args = parse_args()

level = logging.DEBUG if args.debug else logging.INFO

logger = logging.getLogger(__name__)
logger.setLevel(level)
formatter = logging.Formatter(
    fmt='%(asctime)s [%(process)d] %(levelname)s - %(message)s')
handler = logging.StreamHandler()
handler.setLevel(level)
handler.setFormatter(formatter)
logger.addHandler(handler)

auth = OAuth1(
    twitter_consumer_key, twitter_consumer_secret,
    twitter_access_token, twitter_access_token_secret)
evt = StreamEvent()
stream = StreamClient(
    logger_name=__name__, auth=auth, event=evt,
    compressed=args.compressed,
    delimited=args.delimited,
    chunk_size=args.chunk_size,
    stall_warnings=True)

def terminate(signum, frame):
    stream.stop()
signal.signal(signal.SIGTERM, terminate)

try:
    logger.info('Start')
    if isinstance(args.track, str):
        stream.filter(track=args.track, language='ja')
    else:
        stream.sample(language='ja')
except (KeyboardInterrupt, SystemExit):
    stream.stop()
finally:
    evt.report_count(True)
    logger.info('Stop')
