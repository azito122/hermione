# from lib import memory_to_text
from lib import M
import sys

seplength = 100
sepchar = '-'

if __name__ == '__main__':
    memories = M.recall(sys.argv[1])
    print("˅" * seplength)
    for m in memories:
        print(m.render_cli())
        print('')
    print("˄" * seplength)