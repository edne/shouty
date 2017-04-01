from enum import IntEnum


class ShoutErr(IntEnum):
    SUCCESS = 0
    INSANE = -1
    NOCONNECT = -2
    NOLOGIN = -3
    SOCKET = -4
    MALLOC = -5
    METADATA = -6
    CONNECTED = -7
    UNCONNECTED = -8
    UNSUPPORTED = -9
    BUSY = 10
    NOTLS = 11
    TLSBADCERT = -12
    RETRY = -13


class Format(IntEnum):
    OGG = 0
    MP3 = 1
    WEBM = 2
    WEBMAUDIO = 3


class Protocol(IntEnum):
    HTTP = 0
    XAUDIOCAST = 1
    ICY = 2
    ROARAUDIO = 3
