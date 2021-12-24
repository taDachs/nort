from typing import List

import yaml


class Note:
    def __init__(self, name: str, content: str, tags: List[str] = None):
        self.name = name
        self.content = content
        self.tags = tags

    @classmethod
    def from_file(cls, path):
        with open(path, 'r') as f:
            lines = f.readlines()

        meta_started = False
        metadata = ''
        content = ''
        for line in lines:
            if line.strip() == '---' and not meta_started:
                meta_started = True
                continue

            if line.strip() == '---' and meta_started:
                meta_started = False
                continue

            if meta_started:
                metadata += line
            else:
                content += line

        meta = yaml.safe_load(metadata)

        return Note(meta['name'], content, meta['tags'])

    def __repr__(self):
        rep = ''
        rep += '---\n'
        rep += yaml.dump({'name': self.name, 'tags': self.tags})
        rep += '---\n'
        rep += self.content
        return rep

    def __str__(self):
        return repr(self)
