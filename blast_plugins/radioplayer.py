#! /usr/bin/env python3

import datetime
from typing import Dict, Optional, Union
from api import Timeslot, NowPlaying, Track
from blaster import BlastPlugin
import requests

def get_sec(time_str: Optional[str]):
    """Get Seconds from time."""
    if time_str:
      h, m, s = time_str.split(':')
      return int(h) * 3600 + int(m) * 60 + int(s)
    else:
      return 0

class Radioplayer(BlastPlugin):

  def __init__(self):
    # Pull in some config
    self.config = self.get_config('radioplayer')
    if self.config:
      self.last_show = None
      self.last_playing = None

      self.poke_track(None)
    else:
      self.enabled = False

  def poke_show(self, timeslot: Optional[Timeslot]):
    if not self.enabled:
      return
    if (timeslot != self.last_show):
      self.last_show = timeslot

  def poke_track(self, now_playing: Optional[NowPlaying]):
    """
    Now Playing (NP)
    The API also allows clients to submit a concise form of now­playing data that does not use an
    XML document to communicate the content.  Simple request parameters are used instead of an
    XML document.
    https://ingest.radioplayer.co.uk/ingestor/metadata/v1/np/
    The request parameters are as follows
      - rpId ­ the station’s Radioplayer Id
      - startTime ­ the start time of the now playing data in ISO8601 format, UTC timezone
      - duration ­ the duration of the song in seconds
      - title ­ song title, max length 128 characters
      - artist ­ artist name, max length 128 characters
      - description (optional) ­ max length 180 characters
      - imageUrl(optional) ­ Url to an image which will be shown in the search result, must be 86
      x 48 pixels

    A template example of how you could post this data using the commonly found 'curl' command
    line utility follows:
    curl -u yourusername:yourpassword -v --data
    "rpId=YOUR_RPID&startTime=2013-10-01T08:27:00&duration=600&title=SONG
    TITLE&artist=ARTIST" -X POST
    "https://ingest.radioplayer.co.uk/ingestor/metadata/v1/np/"
    """

    if not self.enabled:
      return

    if (now_playing != self.last_playing):
      print("RadioPlayer: Now Playing:", now_playing)
      track: Optional[Track]
      if now_playing and now_playing["track"]:
        track = now_playing["track"]
      elif (self.last_show):
        # Be a bit cheeky and send the current show over as a track.
        track = {
          "title": self.last_show["title"],
          "artist": "URY",
          "length": "00:03:00"
        }
      else:
        track = {
          "title": "",
          "artist": "",
          "length": "00:00:00"
        }
      url = "https://ingest.radioplayer.co.uk/ingestor/metadata/v1/np/"
      auth = (self.config["user"], self.config["pass"])
      # Radioplayer wants UTC. Let's give to 'em.
      start_time = datetime.datetime.utcfromtimestamp(now_playing["start_time"]).isoformat()
      data: Dict[str, Union[str, int]] = {
          "rpId": self.config["rpId"],
          "startTime": start_time,
          "duration": get_sec(track["length"]),
          "title": track["title"],
          "artist": track["artist"]
      }
      r = requests.post(
        url,
        auth = auth,
        data = data
      )
      if r.status_code != 202:
        print("RadioPlayer: Failed to update.\r\nStatus code: {}\r\nData: {}".format(
          r.status_code,
          data
        ))
      self.last_playing = now_playing
