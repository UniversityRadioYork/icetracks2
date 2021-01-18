#! /usr/bin/env python3

from typing import Optional
from api import NowPlaying, Track
from blaster import BlastPlugin
import pylast
import configparser

class LastFM(BlastPlugin):
  last_playing: Optional[NowPlaying]
  config: configparser.SectionProxy
  api: pylast.LastFMNetwork

  def __init__(self):
    # Pull in some config
    config = configparser.ConfigParser()
    config.read('config.ini')
    if "lastfm" in config:
      self.config = config['lastfm']

      self.api = pylast.LastFMNetwork(
        api_key=self.config["api_key"],
        api_secret=self.config["api_secret"],
        username=self.config["user"],
        password_hash=pylast.md5(self.config["pass"])
      )

      self.last_playing = None

      self.poke_track(None)
    else:
      raise Exception("Config for LastFM is missing.")

  def poke_track(self, now_playing: Optional[NowPlaying]):
    if (now_playing != self.last_playing):
      # Scrobble self.last_playing
      if self.last_playing:
        print("LASTFM: Scrobbling: ", self.last_playing)
        track = self.last_playing["track"]
        self.api.scrobble(artist = track["artist"], title = track["title"], timestamp = self.last_playing["start_time"])

      print("LASTFM: Now Playing:", now_playing)
      track: Track
      if now_playing:
        if now_playing["track"] != None:
          track = now_playing["track"]
        else:
          track = {
            "title": "",
            "artist": "",
            "length": None
          }
        self.api.update_now_playing(artist = track["artist"], title = track["title"])
      # Now Playing track
      self.last_playing = now_playing
