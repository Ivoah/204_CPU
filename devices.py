import sys

# from http://code.activestate.com/recipes/134892/
class _Getch:
    '''Gets a single character from standard input.  Does not echo to the
screen.'''
    def __init__(self):
        if sys.platform == 'win32':
            self.impl = _GetchWindows
        else:
            self.impl = _GetchUnix

    def __call__(self): return self.impl()

def _GetchUnix():
    import tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def _GetchWindows():
    import msvcrt
    return msvcrt.getch()

class NullDev:
    def read(self):
        return 0
    
    def write(self, data):
        pass

class IODev:
    def __init__(self):
        self.getch = _Getch()

    def read(self):
        return ord(self.getch())
    
    def write(self, data):
        sys.stdout.write(chr(data))
        sys.stdout.flush()
