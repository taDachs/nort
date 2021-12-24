from typing import List

from ruamel import yaml


class Note:
    def __init__(self, name: str, content: str, tags: List[str] = None):
        self.name = name
        self.content = content
        self.tags = tags

    @classmethod
    def from_file(cls, path):
        meta_started = False
        metadata = ''
        content = ''
        with open(path, 'r') as f:
            for line in f:
                if line.strip() == '---' and not meta_started:
                    meta_started = True
                    continue
                elif line.strip() == '---' and meta_started:
                    meta_started = False
                    break
                metadata += line

            for line in f:
                content += line

        meta = yaml.safe_load(metadata)

        return Note(meta['name'], content, meta['tags'])

    def __repr__(self):
        rep = ''
        rep += '---\n'
        rep += yaml.safe_dump({'name': self.name, 'tags': self.tags})
        rep += '---\n'
        rep += self.content
        return rep

    def __str__(self):
        return repr(self)
