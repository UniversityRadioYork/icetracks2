#! /usr/bin/env python3
'''Handles sending track updates to other services, split from ice.py for a cheap joke.'''

from api import NowPlaying
from typing import Any, List, Optional
import sys
import importlib
import inspect
import pkgutil
import os
import configparser

import blast_plugins


def iter_namespace(ns_pkg):
    # Specifying the second argument (prefix) to iter_modules makes the
    # returned name an absolute name instead of a relative one. This allows
    # import_module to work without having to do additional modification to
    # the name.
    return pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + ".")

class BlastPlugin():
  enabled: bool = True
  last_playing: Optional[NowPlaying]
  config: Optional[configparser.SectionProxy]

  def __init__(self):
    return None

  def poke_track(self, now_playing: Optional[NowPlaying]):
    '''Send new track info to service.'''
    return None

  def get_config(self, section_name: str) -> Optional[configparser.SectionProxy]:

    config = configparser.ConfigParser()
    config.read(os.path.dirname(os.path.realpath(__file__)) + '/config.ini')
    if section_name in config:
      return config[section_name]
    else:
      print("Config for {} is missing.".format(section_name))
      return None


class Blaster():

  plugins: List[BlastPlugin] = []
  def __init__(self):
    # Find blast targets
    plugins = {
        name: importlib.import_module(name)
        for _, name, _
        in iter_namespace(blast_plugins)
    }
    for plugin in plugins:
      classes: List[Any] = [mem[1] for mem in inspect.getmembers(sys.modules[plugin], inspect.isclass) if mem[1].__module__ == sys.modules[plugin].__name__]

      if (len(classes) != 1):
        print(classes)
        raise Exception("Can't import plugin " + plugin + " because it doesn't have 1 class.")

      self.plugins.append(classes[0]())


    print("Discovered blast plugins: ", self.plugins)




  def blast_track(self, now_playing: Optional[NowPlaying]):
    '''Fire track-shaped iceblasts to registered service plugins.'''

    for plugin in self.plugins:
      plugin.poke_track(now_playing)


