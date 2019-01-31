from lib import memory_to_text
from lib import M
import sys

seplength = 50

if __name__ == '__main__':
    memories = M.recall(sys.argv[1])
    print("")
    print("˅" * seplength)
    for m in memories:
        print("." * seplength)
        print("")
        print(memory_to_text(m))
    print("")
    print("˄" * seplength)