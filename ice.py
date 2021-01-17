#! /usr/bin/env python3
'''Handles talking to icecast, to update the playing track.'''

from typing import Optional, Tuple
from api import NowPlaying, Track
import requests


class IceCast():
  url: str
  auth: Tuple[str,str]

  def __init__(self, url: str, auth: Tuple[str,str]):
    self.url = url
    self.auth = auth

  def poke_mount(self, mount: str, now_playing: Optional[NowPlaying]):
    track: Optional[Track] = None
    if now_playing:
      track = now_playing["track"]

    title = "" if not track else track["title"]
    artist = "" if not track else track["artist"]
    url = "{}/admin/metadata?mount=/{}&mode=updinfo&title={}&artist={}".format(self.url, mount, title, artist)
    r = requests.get(
      url,
      auth = self.auth
    )
    print(r)
