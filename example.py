#!/usr/bin/env python3
from sys import argv
import logging
import shouty

logging.basicConfig(level=logging.DEBUG)


params = {
    'host': 'localhost',
    'port': 8000,
    'user': 'source',
    'password': 'hackme',
    'format': shouty.Format.MP3,
    'mount': '/shouty',
    'audio_info': {
        'channels': '2'
    }
}

try:
    with shouty.connect(**params) as connection:
        for file_name in argv[1:]:
            connection.send_file(file_name)
except KeyboardInterrupt:
    print()
