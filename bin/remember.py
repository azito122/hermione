# from lib import text_to_memory
from lib import Mind
from lib import Memory
import sys

M = Mind()

if __name__ == '__main__':
    text = sys.argv[1]
    id = sys.argv[2] if len(sys.argv) > 2 else None
    mem = Memory.from_text(None, text)
    mem.id = id
    M.remember(mem)