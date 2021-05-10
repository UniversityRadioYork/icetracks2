#! /usr/bin/env python3
'''Handles talking to the MyRadio API to get track info.'''

from typing import List, Optional
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from enum import Enum
import datetime
from typing_extensions import TypedDict


class Source(Enum):
  a = "API (Unspecified)"
  b = "BAPS",
  j = "Jukebox",
  m = "Manual",
  o = "Other",
  s = "Sequencer",
  w = "WebStudio",

  def __repr__(self) -> str:
      return '"' + self.name + '"'

class Track(TypedDict):
  title: str
  artist: str
  length: Optional[str]

class NowPlaying(TypedDict):
  start_time: int
  track: Track

class Timeslot(TypedDict):
  title: str
  photo: Optional[str]
  startTime: int
  endTime: str
  realShow: bool
class API():

  transport: RequestsHTTPTransport
  client: Client

  def __init__(self, url_base: str, url: str, api_key: str):

    # Select your transport with a defined url endpoint
    self.transport = RequestsHTTPTransport(url + "?api_key=" + api_key)

    # Create a GraphQL client using the defined transport
    self.client = Client(transport=self.transport, fetch_schema_from_transport=True)

    self.url_base = url_base

  def getNowPlaying(self, sources: Optional[List[Source]] = None, allow_off_air: Optional[bool] = None) -> Optional[NowPlaying]:

    params = []
    if (sources):
      params.append("sources: " + str(sources))

    if (allow_off_air != None):
      params.append("allowOffAir: " + str(allow_off_air).lower())

    if (params):
      params = "(" + ",".join(params) + ")"
    else:
      params = ""

    query = gql(
      '''
        query {{
          nowPlaying {} {{
            startTime: start_time
            track {{
              ... on Track {{
                title
                artist
                length
              }}
              ... on TrackNotRec {{
                title
                artist
              }}
            }}
          }}
        }}
      '''.format(params)
    )

    #try:
    response: Optional[NowPlaying] = self.client.execute(query)
    #except:
    #  raise # TODO: Log this.
    #  return None

    if response != None:
      if ("nowPlaying" in response and response["nowPlaying"]):
        start_time: int = int(datetime.datetime.fromisoformat(response["nowPlaying"]["startTime"]).timestamp())
        track: Track = response["nowPlaying"]["track"]

        nowPlaying: NowPlaying = {
          "start_time": start_time,
          "track": track
        }
        return nowPlaying
    return None

  def getCurrentShow(self):
    query = gql(
      '''
        query {
            currentAndNext {
                current {
                  ... on Timeslot {
                    title
                    photo
                    startTime
                    endTime
                    webpage
                    id
                  }
                }
              }
        }
      '''
    )
    response = self.client.execute(query)
    if "currentAndNext" in response and response["currentAndNext"]["current"]:
      current = response["currentAndNext"]["current"]
      endTime: int = -1
      try:
        endTime: int = int(datetime.datetime.fromisoformat(response["nowPlaying"]["endTime"]).timestamp())
      except:
        pass

      current_show: Timeslot = {
        "title": str(current["title"]),
        "photo": self.url_base + str(current["photo"]),
        "startTime": int(datetime.datetime.fromisoformat(current["startTime"]).timestamp()),
        "endTime": endTime,
        "webpage": self.url_base + current["webpage"] if "webpage" in current else None,
        "realShow": "id" in current
      }
      return current_show
    return None
