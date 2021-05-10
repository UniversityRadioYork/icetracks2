#! /usr/bin/env python3
'''Handles talking to icecast, to update the playing track.'''

from typing import Optional, Tuple
from api import NowPlaying, Track
import requests
from urllib.parse import urlencode, quote_plus

from urllib.parse import urlencode, quote_plus

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

    title = "URY" if not track else track["title"]
    artist = " " if not track else track["artist"]
    params = {
        'title': title,
        'artist': arist,
        'mode': "updinfo"
    }
    encoded = urlencode(params, quote_via=quote_plus)
    url = "{}/admin/metadata?mount=/{}{}".format(self.url, mount, encoded)
    r = requests.get(
      url,
      auth = self.auth
    )
    if r.status_code != 200:
      print("Icecast: Failed to update.\r\nStatus code: {}\r\nURL: {}".format(
        r.status_code,
        url
      ))
