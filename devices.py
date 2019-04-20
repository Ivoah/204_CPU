import sys
import pygame
from pygame.locals import *

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
        if ch == '\x03':
            raise KeyboardInterrupt
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

class VideoDev:
    def __init__(self):
        self.window = pygame.display.set_mode((256, 256))
        pygame.display.flip()
        self.x = None
        self.y = None
        self.pressed = None
    
    def read(self):
        for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit(0)
                elif event.type == KEYDOWN and event.key <= 255:
                    self.pressed = event.key
                elif event.type == KEYUP and event.key <= 255:
                    self.pressed = None
        
        return self.pressed or 0
    
    def write(self, data):
        for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit(0)
        if self.x is None:
            self.x = data
        elif self.y is None:
            self.y = data
        else:
            c = pygame.Color((data >> 5)*36, (data >> 2 & 0b111)*36, (data & 0b11)*85)
            self.window.set_at((self.x, self.y), c)
            pygame.display.flip()
            self.x = None
            self.y = None
