from lib import text_to_memory
from lib import Mind
import sys

M = Mind()

if __name__ == '__main__':
    text = sys.argv[1]
    mem = text_to_memory(text)
    M.remember(mem)