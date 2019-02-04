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
    def __init__(self, body, tags, t):
        self.body = body
        self.tags = tags
        self.time = t

    def get_rendered(self):
        mtime = float(self.time)
        t = datetime.datetime.fromtimestamp(mtime)
        t = t.strftime("%m/%d/%Y %I:%M %p")
        return {
            'tags': ' '.join(self.tags),
            'body': self.body,
            'time': t
        }

    def render_cli(self, sepcount = 100, sepchar = '-'):
        rendered = self.get_rendered()
        o = ""
        o += (sepchar * (sepcount//2)) + rendered['time'] + (sepchar * (sepcount//2))
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
        tags = re.findall(tagpat, text)
        body = re.sub(tagpat, '', text).strip()
        t = time.time()
        return Memory(body, tags, t)

class Mind:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read(resolvepath('~/hermione/hermione.conf'))
        self.dbpath = resolvepath(config['DEFAULT']['dbpath'])
        self.db = TinyDB(self.dbpath, sort_keys=True, indent=4, separators=(',', ': '))

    def remember(self, memory):
        self.db.insert({
            'tags': memory.tags,
            'body': memory.body
        })

    def recall(self, search):
        memory = Query()
        if search.find('#') == 0:
            memories = self.db.search(memory.tags.any([search]))
        else:
            memories = self.db.search(memory.body.search(search))
        memories = [Memory(m['body'], m['tags'], (m['time'] if 'time' in m else '(no time stored)')) for m in memories]
        return memories

M = Mind()