from contextlib import contextmanager
from .connection import Connection


@contextmanager
def connect(**kwargs):
    cn = Connection(**kwargs)
    cn.open()
    yield cn
    cn.close()
    cn.free()

# TODO: here the other functions to expose
