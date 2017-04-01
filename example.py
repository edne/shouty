#!/usr/bin/env python3
from sys import argv
import shouty


params = {
    'user': 'source',
    'password': 'hackme',
    'format': shouty.SHOUT_FORMAT_MP3,
    'mount': '/shouty'
}

try:
    with shouty.connect(**params) as connection:
        for file_name in argv[1:]:
            connection.send_file(file_name)
except KeyboardInterrupt:
    print()
