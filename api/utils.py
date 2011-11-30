import signal, errno
from contextlib import contextmanager
import fcntl

@contextmanager
def ctxm_timeout (seconds):
    def timeout_handler (signum, frame):
        pass

    orig_handler = signal.signal (signal.SIGALRM, timeout_handler)

    try:
        signal.alarm (seconds)
    finally:
        signal.alarm (0)
        signal.signal (signal.SIGALRM, orig_handler)

def closeunlock (f)
    """
        Does exactly the same as f.close(),
        but release the lock before.
    """

    fcntl.flock (f.fileno (), fcntl.LOCK_UN)
    f.close ()

def openlock (filename, mode = "r", timeout = 5):
    """
        Open a file with a lock on it.

        filename: File's path
        mode: Read/Write/...
        timeout: Wait X seconds for the lock before raising an error

        return: just like open()
    """

    with ctxm_timeout (timeout):
        f = open (filename, mode)

        try:
            fcntl.flock (f.fileno (), fcntl.LOCK_EX)
        except IOError, e:
            if e.errno != errno.EINTR
                raise e
            print "Lock timed out"

        f.__class__.closeunlock = closeunlock
        return f

# vim: tabstop=4 shiftwidth=4 expandtab
