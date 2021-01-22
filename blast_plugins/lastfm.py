#! /usr/bin/env python3

from typing import Optional
from api import NowPlaying, Track
from blaster import BlastPlugin
import pylast

class LastFM(BlastPlugin):

  api: pylast.LastFMNetwork

  def __init__(self):
    # Pull in some config
    self.config = self.get_config('lastfm')
    if self.config:

      self.api = pylast.LastFMNetwork(
        api_key=self.config["api_key"],
        api_secret=self.config["api_secret"],
        username=self.config["user"],
        password_hash=pylast.md5(self.config["pass"])
      )

      self.last_playing = None

      self.poke_track(None)
    else:
      self.enabled = False

  def poke_track(self, now_playing: Optional[NowPlaying]):
    if not self.enabled:
      return

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
