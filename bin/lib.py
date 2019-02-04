from tinydb import TinyDB, Query
import configparser
import re
import os
import datetime
import time

def resolvepath(path):
    path = os.path.expanduser(path)
    if path.find('/') != 0:
        path = os.path.realpath('..') + '/' + path
    return path

class Memory:
    def __init__(self, data):
        self.id   = data['id'] if 'id' in data else None
        self.body = data['body']
        self.tags = data['tags']
        self.time = data['time']

    def get_rendered(self):
        mtime = float(self.time)
        t = datetime.datetime.fromtimestamp(mtime)
        t = t.strftime("%m/%d/%Y %I:%M %p")
        return {
            'tags': ' '.join(self.tags),
            'body': self.body,
            'time': t,
            'id': self.id,
        }

    def render_cli(self, sepcount = 100, sepchar = '-'):
        idcolor = '\033[1;33m'
        nocolor = '\033[0m'
        rendered = self.get_rendered()
        o = ""
        t = str(rendered['time'])
        id = str(rendered['id'])
        mid = '( \033[0;31m' + idcolor + id + nocolor + ' | ' + t + ' )'
        sepcount = sepcount - len(mid)
        o += (sepchar * (sepcount//2)) + mid + (sepchar * (sepcount//2))
        o += "\n"
        o += rendered['tags']
        o += "\n\n"
        o += rendered['body']
        return o

    def render_vim(self):
        r = self.get_rendered()
        o = ""
        o += r['tags']
        o += "\n\n"
        o += r['body']
        return o

    def from_text(self, text):
        tagpat = r'#[a-zA-Z0-9-_]+'
        return Memory({
            'body': re.sub(tagpat, '', text).strip(),
            'tags': re.findall(tagpat, text),
            'time': time.time()
        })

class Mind:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read(resolvepath('~/hermione/hermione.conf'))
        self.dbpath = resolvepath(config['DEFAULT']['dbpath'])
        self.db = TinyDB(self.dbpath, sort_keys=True, indent=4, separators=(',', ': '))

    def remember(self, memory):
        if memory.id is not None:
            print(memory.id)
            Q = Query()
            self.db.update({
                'tags': memory.tags,
                'body': memory.body,
                # 'time': memory.time,
            }, None, [int(memory.id)])
        else:
            self.db.insert({
                'tags': memory.tags,
                'body': memory.body,
                'time': memory.time
            })

    def recall_by_id(self, id):
        M = Query()
        mem = self.db.get(M, id)
        return Memory({
            'body': mem['body'],
            'tags': mem['tags'],
            'time': mem['time'],
            'id': mem.doc_id
        })

    def recall(self, search):
        memory = Query()
        if search.find('#') == 0:
            memories = self.db.search(memory.tags.any([search]))
        else:
            memories = self.db.search(memory.body.search(search))
        memories = [Memory({
            'body': m['body'],
            'tags': m['tags'],
            'time': m['time'],
            'id': m.doc_id}
        ) for m in memories]
        return memories

M = Mind()