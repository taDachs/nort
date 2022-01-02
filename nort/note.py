from typing import List
from datetime import datetime
import re

from ruamel import yaml


class SectionNotFoundException(Exception):
    pass


class Note:
    def __init__(self,
                 name: str,
                 content: str,
                 tags: List[str] = None,
                 created=None):
        self.name = name
        self.content = content
        self.tags = tags
        self.file_name = name if '.md' == name[-3:] else name + '.md'
        if created:
            self.created = created
        else:
            self.created = datetime.now()

    def get_section(self, title: str) -> str:
        lines = self.content.split('\n')
        section = ''
        started = False
        for line in lines:
            if re.match(r'#* \w*', line.strip()):
                section_title = line.replace('#', '').strip()
                if section_title == title:
                    started = True
                else:
                    started = False
            if started:
                section += line + '\n'

        if not section:
            raise SectionNotFoundException(f'Section {title} not found')

        return section

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

        return Note(meta['name'], content, meta['tags'], meta['created'])

    def __str__(self):
        rep = ''
        rep += '---\n'
        rep += yaml.safe_dump({
            'name': self.name,
            'tags': self.tags,
            'created': self.created
        })
        rep += '---\n'
        rep += self.content
        return rep
