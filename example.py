#!/usr/bin/env python3
from sys import argv
from shout import Shout, SHOUT_FORMAT_MP3


shout = Shout(user='source', password='hackme',
              format=SHOUT_FORMAT_MP3,
              mount='/shouty')

try:
    with shout.connect():
        for file_name in argv[1:]:
            shout.send_file(file_name)
except KeyboardInterrupt:
    print()
