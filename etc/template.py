# This is a example template file
# place it under ~/.config/nort/template.py

from nort.template import Template
from nort.note import SectionNotFoundException
from nort.nort import list_notes


def get_last_note(tags):
    notes = list_notes(cfg=Template.cfg, tags=tags)
    if not notes:
        return None
    notes.sort(key=lambda x: x.created, reverse=True)
    return notes[0]


def last_todo(tags):
    note = get_last_note(tags)
    if not note:
        return '## TODO'

    try:
        return note.get_section('TODO')
    except SectionNotFoundException:
        return '## TODO'


class Diary(Template):
    def get_name(self):
        return 'Diary_[[DATE]]'

    def get_tags(self):
        return ['diary', 'todo', '[[DATE]]']

    def get_content(self):
        return '\n'.join([
            '# [[DATE]]',
            '',
            last_todo(['diary', 'todo']),
        ])


class Work(Template):
    def __init__(self, job='Work'):
        super().__init__()
        self.job = job

    def get_name(self):
        return f'{self.job}_[[DATE]]'

    def get_tags(self):
        return ['work', self.job.lower(), '[[DATE]]', 'todo', 'daybook']

    def get_content(self):
        return '\n'.join([
            f'# {self.job} on [[DATE]]',
            '',
            '| started | finished | break |',
            '|---------|----------|-------|',
            '| [[TIME]]| TODO     | TODO  |',
            '',
            last_todo(['work', 'todo', self.job.lower(), 'daybook']),
        ])
