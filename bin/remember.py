# from lib import text_to_memory
from lib import Mind
from lib import Memory
import sys

M = Mind()

if __name__ == '__main__':
    text = sys.argv[1]
    print(text)
    mem = Memory.from_text(None, text)
    M.remember(mem)