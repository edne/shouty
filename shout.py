#!/usr/bin/env python3
from contextlib import contextmanager
import atexit
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
    err = f(obj, s.encode('ascii'))
    if err != SHOUTERR_SUCCESS:
        raise Exception('Failed set_string, error: ' + str(err))


def set_int(obj, f, n):
    f.argtypes = [ctypes.c_void_p, ctypes.c_int]
    err = f(obj, n)
    if err != SHOUTERR_SUCCESS:
        raise Exception('Failed set_int, error: ' + str(err))


lib = ctypes.CDLL(so_file)
lib.shout_init()
atexit.register(lib.shout_shutdown)


class Shout:
    def __init__(self,
                 host='localhost', port=8000,
                 user='source', password='',
                 protocol=SHOUT_PROTOCOL_HTTP,
                 format=SHOUT_FORMAT_OGG,
                 mount='/shouty'):

        lib.shout_new.restype = ctypes.c_void_p
        self.obj = lib.shout_new()
        if not self.obj:
            raise Exception('Memory error')

        set_int(self.obj, lib.shout_set_port, port)
        set_string(self.obj, lib.shout_set_host, host)

        set_string(self.obj, lib.shout_set_user, user)
        set_string(self.obj, lib.shout_set_password, password)

        set_int(self.obj, lib.shout_set_protocol, protocol)
        set_int(self.obj, lib.shout_set_format, format)
        set_string(self.obj, lib.shout_set_mount, mount)

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
        lib.shout_send.argtypes = [ctypes.c_void_p,
                                   ctypes.c_char_p,
                                   ctypes.c_size_t]
        lib.shout_sync.argtypes = [ctypes.c_void_p]
        lib.shout_close.argtypes = [ctypes.c_void_p]
        lib.shout_free.argtypes = [ctypes.c_void_p]

    @contextmanager
    def connect(self):
        self.open()
        yield
        self.close()

    def open(self):
        err = lib.shout_open(self.obj)
        if err != SHOUTERR_SUCCESS:
            raise Exception('Failed shout_open, error: ' + str(err))

    def send(self, chunk):
        err = lib.shout_send(self.obj, chunk, len(chunk))
        if err != SHOUTERR_SUCCESS:
            raise Exception('Failed shout_send, error: ' + str(err))

    def sync(self):
        err = lib.shout_sync(self.obj)
        if err != SHOUTERR_SUCCESS:
            raise Exception('Failed shout_sync, error: ' + str(err))

    def close(self):
        err = lib.shout_close(self.obj)
        if err != SHOUTERR_SUCCESS:
            raise Exception('Failed shout_close, error: ' + str(err))

    def send_file(self, file_name):
        print(file_name)
        with open(file_name, 'rb') as f:
            while True:
                chunk = f.read(4096)
                if not chunk:
                    break

                shout.send(chunk)
                shout.sync()

    def __del__(self):
        lib.shout_free(self.obj)


shout = Shout(user='source', password='hackme',
              format=SHOUT_FORMAT_MP3,
              mount='/shouty')

try:
    with shout.connect():
        for file_name in argv[1:]:
            shout.send_file(file_name)
except KeyboardInterrupt:
    print()
