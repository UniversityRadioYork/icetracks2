#! /usr/bin/env python3
'''Main loop for Icetracks 2, codenamed Iceblaster'''
import time
from typing import List, Optional
from api import API, Source
from blaster import Blaster
from ice import IceCast
import configparser

class IceTracks():

  api: API
  blaster: Blaster
  ice: IceCast
  mounts: List[str]


  def __init__(self):
    # Pull in some config
    config = configparser.ConfigParser()
    config.read('config.ini')
    self.mounts = config["icecast"]["mounts"].replace(" ", "").split(",")

    self.api = API(url = config["myradio"]["url"], api_key=config["myradio"]["api_key"])
    self.blaster = Blaster()
    self.ice = IceCast(url = config["icecast"]["url"], auth=(config["icecast"]["user"], config["icecast"]["pass"]))
    print("Welcome to IceTracks!")
    self.loop()

  def loop(self):
    while True:

      # Push default now playing API output to all configured icecast mounts.
      nowPlaying = self.api.getNowPlaying()

      self.blaster.blast_track(nowPlaying)

      print("Live is Playing: ", nowPlaying)
      for mount in self.mounts:
        self.ice.poke_mount(mount, nowPlaying)


      # Now for currently hardcoded source -> mount mappings.
      jukebox = self.api.getNowPlaying(sources=[Source.j], allow_off_air=True)
      print("\nJukebox is Playing: ", jukebox)
      self.ice.poke_mount("jukebox", jukebox)

      time.sleep(15)
      print("\n")

if __name__ == "__main__":
  iceblaster = IceTracks()
