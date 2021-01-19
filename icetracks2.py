#! /usr/bin/env python3
'''Main loop for Icetracks 2, codenamed Iceblaster'''
import time
from typing import List
from api import API, Source
from blaster import Blaster
from ice import IceCast
import configparser
import os

class IceTracks():

  api: API
  blaster: Blaster
  ice: IceCast
  mounts: List[str]


  def __init__(self):
    # Pull in some config
    config = configparser.ConfigParser()
    config.read(os.path.dirname(os.path.realpath(__file__)) + '/config.ini')
    self.mounts = config["icecast"]["mounts"].replace(" ", "").split(",")

    self.api = API(url = config["myradio"]["url"], api_key=config["myradio"]["api_key"])
    self.blaster = Blaster()
    self.ice = IceCast(url = config["icecast"]["url"], auth=(config["icecast"]["user"], config["icecast"]["pass"]))
    print("Welcome to IceTracks!")
    self.loop()

  def loop(self):
    while True:
      try:
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

        webstudio = self.api.getNowPlaying(sources=[Source.w], allow_off_air=True)
        print("\nWebstudio is Playing: ", webstudio)
        self.ice.poke_mount("webstudio", webstudio)

      # General Catch All. Ideally we never crash, rather just ignore updates caused by exceptions
      except Exception as e:
        print("Failure, will try again in next loop. Exception: ", e)

      time.sleep(15)
      print("\n")

if __name__ == "__main__":
  iceblaster = IceTracks()
