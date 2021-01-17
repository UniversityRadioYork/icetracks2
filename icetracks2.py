#! /usr/bin/env python3
'''Main loop for Icetracks 2, codenamed Iceblaster'''
import time
from api import API, Source
from blaster import Blaster
from ice import IceCast
import configparser

class IceTracks():

  api: API
  blaster: Blaster
  ice: IceCast


  def __init__(self):
    # Pull in some config
    config = configparser.ConfigParser()
    config.read('config.ini')

    self.api = API(url = config["myradio"]["url"], api_key=config["myradio"]["api_key"])
    self.blaster = Blaster()
    self.ice = IceCast(url = config["icecast"]["url"], auth=(config["icecast"]["user"], config["icecast"]["pass"]))
    print("Welcome to IceTracks!")
    self.loop()

  def loop(self):
    while True:
      nowPlaying = self.api.getNowPlaying()

      self.blaster.blast_track(nowPlaying)

      print("Live is Playing: ", nowPlaying)
      self.ice.poke_mount("am", nowPlaying)
      print("Jukebox is Playing: ", self.api.getNowPlaying(sources=[Source.j], allow_off_air=True))

      time.sleep(15)

if __name__ == "__main__":
  iceblaster = IceTracks()
