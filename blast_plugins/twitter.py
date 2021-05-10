#! /usr/bin/env python3
'''Tweetbot plugin, pushes the current playing track to a twitter handle near you! Originally by Colin Roit.'''
from typing import Optional
from api import NowPlaying, Timeslot, Track
from blaster import BlastPlugin
import tweepy
import random
class TwitterBot(BlastPlugin):

    twitter_api: tweepy.API

    def __init__(self):
        # Pull in some config
        self.config = self.get_config('twitter')
        self.general_config = self.get_config('general')
        if self.config:
            auth = tweepy.OAuthHandler(
                self.config['consumer_key'],
                self.config['consumer_secret']
            )
            auth.set_access_token(
                self.config['token'],
                self.config['token_secret']
            )
            self.twitter_api = tweepy.API(auth)
            self.last_playing = None
            self.last_show = None
            self.poke_show(None)
            self.poke_track(None)
        else:
            self.enabled = False

    def poke_track(self, now_playing: Optional[NowPlaying]):
        if not self.enabled:
            return

        emoji = '🎵'

        if (now_playing != self.last_playing):
            print("Twitter: Now Playing:", now_playing)
            track: Track
            if now_playing and now_playing["track"] != None:
                track = now_playing["track"]
                # Tweet
                songText = track['title'] + ' - ' + track['artist']
                tweet = emoji*2 + ' NOW PLAYING: ' + songText + ' ' + emoji*2
                try:
                    self.twitter_api.update_status(tweet)
                except tweepy.TweepError as e:
                    # Catch stuff like Duplicate Tweets etc.
                    print("ERROR: ", e)
            self.last_playing = now_playing

    def poke_show(self, timeslot: Optional[Timeslot]):
        if not self.enabled:
            return

        short_name = self.general_config["short_name"]
        intros = ["Coming up now on {}:".format(short_name), "Listen now on {} for ".format(short_name), "Listen live NOW for "]
        emojis = ['🎤','🎧','📻','🎙']

        rand = random.randrange(0, len(emojis))
        intro = intros[rand]
        emoji = emojis[rand]


        if (timeslot != self.last_show and timeslot):
            if (timeslot["realShow"]):
                url: str = timeslot["url"] if "url" in timeslot else ""
                tweet: str = '{} {}{} {}\n{}'.format(emoji*2, intro, timeslot["title"], emoji*2, url)
                try:
                    self.twitter_api.update_status(tweet)
                except tweepy.TweepError as e:
                    # Catch stuff like Duplicate Tweets etc.
                    print("ERROR: ", e)
