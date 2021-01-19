# icetracks2
Codenamed **Iceblaster**, this is a rewrite of (private project) Icetracks, this time with 100% more Python.

## What does it do?
It takes URY MyRadio's Now Playing API and blasts track-shaped metadata to various services that appreciate knowing what URY's playing.

Currently, these services are:
- Icecast
- RadioPlayer
- LastFM
- Twitter ([@URYNowPlaying](https://twitter.com/urynowplaying))

## How to run it?

It will want Python3 of some description. Tested on 3.7.

1. Copy `config.dist.ini` to `config.ini` and fill in the details. Leaving out the config for one of the plugins should disable that plugin for you.

2. Run `pip3 install -r requirements.txt` to get the few requirements you need.

3. Run `python3 ./icetracks2.py`

A systemd service and env instructions will follow soon.


