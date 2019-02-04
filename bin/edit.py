from lib import M
import sys

if __name__ == '__main__':
    id = int(sys.argv[1])
    memory = M.recall_by_id(id)
    f = open('/tmp/hermione', 'w+')
    f.write(memory.render_vim())
    print(id)
