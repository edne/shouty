#!/usr/bin/env python3
from sys import argv
import ctypes
import ctypes.util

so_file = ctypes.util.find_library('shout')

if not so_file:
    # TODO raise something
    pass

lib = ctypes.CDLL(so_file)

lib.shout_init()

lib.shout_new.restype = ctypes.c_void_p
obj = lib.shout_new()

# host - default localhost
host = 'localhost'
lib.shout_set_host.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
lib.shout_set_host(obj, host.encode('ascii'))

# port - default 8000
lib.shout_set_port.argtypes = [ctypes.c_void_p, ctypes.c_int]
lib.shout_set_port(obj, 8000)

# user - default source
lib.shout_set_user.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
lib.shout_set_user(obj, b'source')

# password - NO default, must be set
lib.shout_set_password.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
lib.shout_set_password(obj, b'hackme')

SHOUT_PROTOCOL_HTTP = 0
SHOUT_PROTOCOL_XAUDIOCAST = 1
SHOUT_PROTOCOL_ICY = 2
SHOUT_PROTOCOL_ROARAUDIO = 3

# protocol - default http
lib.shout_set_protocol.argtypes = [ctypes.c_void_p, ctypes.c_int]
lib.shout_set_protocol(obj, SHOUT_PROTOCOL_HTTP)

SHOUT_FORMAT_OGG = 0
SHOUT_FORMAT_MP3 = 1
SHOUT_FORMAT_WEBM = 2
SHOUT_FORMAT_WEBMAUDIO = 3

# format - default ogg
lib.shout_set_format.argtypes = [ctypes.c_void_p, ctypes.c_int]
lib.shout_set_format(obj, SHOUT_FORMAT_MP3)

# mount - SHOUT_PROTOCOL_ICY doesn't support it
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
