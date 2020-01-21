import tty
import select
import termios
from sys import stdin

def raw_keyboard_key():
    if select.select([stdin], [], [], 0) == ([stdin], [], []):
        return stdin.read(1)

old_settings = termios.tcgetattr(stdin)

try:
    tty.setcbreak(stdin.fileno())
    while True:
        print("Loop")
        key = raw_keyboard_key()
        print(key)
        if key == '\x1b':
            break
finally:
    termios.tcsetattr(stdin, termios.TCSADRAIN, old_settings)