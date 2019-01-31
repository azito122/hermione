from tinydb import TinyDB, Query
import configparser
import re
import os

def resolvepath(path):
    if path.find('/') == 0:
        return path
    else:
        return os.path.realpath('..') + '/' + path

class Memory:
    def __init__(self, tags, body):
        self.tags = tags
        self.body = body

class Mind:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('../hermione.conf')
        self.dbpath = resolvepath(config['DEFAULT']['dbpath'])
        self.db = TinyDB(self.dbpath)

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
        memories = [Memory(m['tags'], m['body']) for m in memories]
        return memories

def text_to_memory(text):
    tagpat = r'#[a-zA-Z0-9-_]+'
    tags = re.findall(tagpat, text)
    body = re.sub(tagpat, '', text).strip()
    return Memory(tags, body)

def memory_to_text(memory):
    tags = ' '.join(memory.tags)
    text = tags
    text += "\n\n"
    text += memory.body
    return text

M = Mind()