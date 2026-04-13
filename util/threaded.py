from threading import Thread

import functools
def threaded(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        thread = Thread(target=fn, args=args, kwargs=kwargs).start()
        return thread
    return wrapper