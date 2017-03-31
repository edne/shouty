#!/usr/bin/env python3
from sys import argv
import ctypes
import ctypes.util

# shout.h enums:
SHOUTERR_SUCCESS = 0
SHOUTERR_INSANE = -1
SHOUTERR_NOCONNECT = -2
SHOUTERR_NOLOGIN = -3
SHOUTERR_SOCKET = -4
SHOUTERR_MALLOC = -5
SHOUTERR_METADATA = -6
SHOUTERR_CONNECTED = -7
SHOUTERR_UNCONNECTED = -8
SHOUTERR_UNSUPPORTED = -9
SHOUTERR_BUSY = 10
SHOUTERR_NOTLS = 11
SHOUTERR_TLSBADCERT = -12
SHOUTERR_RETRY = -13

SHOUT_FORMAT_OGG = 0
SHOUT_FORMAT_MP3 = 1
SHOUT_FORMAT_WEBM = 2
SHOUT_FORMAT_WEBMAUDIO = 3

SHOUT_PROTOCOL_HTTP = 0
SHOUT_PROTOCOL_XAUDIOCAST = 1
SHOUT_PROTOCOL_ICY = 2
SHOUT_PROTOCOL_ROARAUDIO = 3
#

so_file = ctypes.util.find_library('shout')

if not so_file:
    # TODO raise something
    pass


def set_string(obj, f, s):
    f.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
    f(obj, s.encode('ascii'))


def set_int(obj, f, n):
    f.argtypes = [ctypes.c_void_p, ctypes.c_int]
    f(obj, n)


lib = ctypes.CDLL(so_file)

lib.shout_init()

lib.shout_new.restype = ctypes.c_void_p
obj = lib.shout_new()

set_string(obj, lib.shout_set_host, 'localhost')
set_int(obj, lib.shout_set_port, 8000)
set_string(obj, lib.shout_set_user, 'source')
set_string(obj, lib.shout_set_password, 'hackme')
set_int(obj, lib.shout_set_protocol, SHOUT_PROTOCOL_HTTP)
set_int(obj, lib.shout_set_format, SHOUT_FORMAT_MP3)
set_string(obj, lib.shout_set_mount, '/shouty')

# dumpfile
# agent

# Directory parameters, all optional:
# public
# name
# url
# genre
# description
# audio_info

lib.shout_open.argtypes = [ctypes.c_void_p]
lib.shout_open(obj)
# TODO: get error code


lib.shout_send.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_size_t]
lib.shout_sync.argtypes = [ctypes.c_void_p]
lib.shout_close.argtypes = [ctypes.c_void_p]

for file_name in argv[1:]:
    print(file_name)
    with open(file_name, 'rb') as f:
        while True:
            chunk = f.read(4096)
            if not chunk:
                break

            lib.shout_send(obj, chunk, len(chunk))
            lib.shout_sync(obj)

        lib.shout_close(obj)

lib.shout_free.argtypes = [ctypes.c_void_p]
lib.shout_free(obj)

lib.shout_shutdown()
