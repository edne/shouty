#!/usr/bin/env python3
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


lib.shout_set_port.argtypes = [ctypes.c_void_p, ctypes.c_int]
lib.shout_set_port(obj, 8000)

lib.shout_free.argtypes = [ctypes.c_void_p]
lib.shout_free(obj)

lib.shout_shutdown()
