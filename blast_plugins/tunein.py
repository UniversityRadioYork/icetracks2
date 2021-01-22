#! /usr/bin/env python3

from typing import Dict, Optional
from api import NowPlaying, Track
from blaster import BlastPlugin
import requests

class TuneIn(BlastPlugin):

  def __init__(self):
    # Pull in some config
    self.config = self.get_config('tunein')
    if self.config:
      self.last_playing = None

      self.poke_track(None)
    else:
      self.enabled = False

  def poke_track(self, now_playing: Optional[NowPlaying]):
    """
    Requests to the AIR API are very simple. An example call appears as follows…

    GET http://air.radiotime.com/Playing.ashx?partnerId=&partnerKey=&id=&title=Bad+Romance&artist=Lady+Gaga

    Your partnerId replaces , partnerKey replaces , and stationId, including the preliminary ‘s’ replaces . Your title and artist information should be set to be updated by your broadcast software in correspondence with the currently playing song.

    Output:
    Check the status code for success or failure result (200 means success)

    NOTES
    For now playing updates, please submit only once at the start of the song. Do not use a timer to submit a song, or submit a song multiple times.
    Your requests may be blocked if you send multiple requests within a short period. Make sure to include an “s” before your station ID.
    Information does not update on the TuneIn.com site in real-time. Changes to station information can take up to a day to appear.

    If the station is going to a commercial or other non-song playing period, send the request with the commercial=true flag.

    """

    if not self.enabled:
      return

    if (now_playing != self.last_playing):
      print("TuneIn: Now Playing:", now_playing)
      track: Optional[Track]
      if now_playing:
        if now_playing["track"] != None:
          track = now_playing["track"]
        else:
          track = None

        url = "http://air.radiotime.com/Playing.ashx"
        data: Dict[str, str] = {
          "partnerId": self.config["partnerId"],
          "partnerKey": self.config["partnerKey"],
          "commercial": "false"
        }
        if track:
          data["title"] = track["title"]
          data["artist"] = track["artist"]
        else:
          data["commercial"] = "true"

        r = requests.get(
          url,
          params = data
        )
        if r.status_code != 200:
          print("Tunein: Failed to update.\r\nStatus code: {}\r\nData: {}".format(
            r.status_code,
            data
          ))
      self.last_playing = now_playing
