import os
from typing import List

from .config import Config
from .note import Note
from .template import template_by_name


class NoteExistsException(Exception):
    pass


def get_note_name(cfg: Config, name: str = None, template: str = None) -> str:
    if name:
        return name
    else:
        if not template:
            raise ValueError('Missing name')
        note = template_by_name(template, cfg).to_note()
        return note.name


def load_note_by_name(name: str, cfg: Config) -> Note:
    file_name = name if '.md' == name[-3:] else name + '.md'

    path = os.path.join(cfg.notes_path, file_name)
    if not os.path.isfile(path):
        raise ValueError(f'File {path} does not exist')
    note = Note.from_file(path)
    return note


def get_filename(template: str, name: str, cfg: Config, **kwargs) -> str:
    if template and name:
        raise ValueError(
            'Can\'t use both name and template argument in same command')

    note_name = get_note_name(cfg=cfg, name=name, template=template)
    file_name = note_name if '.md' == note_name[-3:] else note_name + '.md'

    path = os.path.join(cfg.notes_path, file_name)

    if not os.path.isfile(path):
        raise ValueError(f'{name if name else path} does not exist')

    return path


def new_note(template: str,
             name: str,
             cfg: Config,
             tags: List[str] = None,
             override: bool = False,
             **kwargs) -> str:
    if not tags:
        tags = []

    name = get_note_name(cfg, name, template)

    if template:
        note = template_by_name(template, cfg).to_note()
        note.name = name
        note.tags += tags
    else:
        if not name:
            raise ValueError('missing name')
        tags = tags
        note = Note(name=name, content=f'# {name}', tags=tags)

    file_name = name if '.md' == name[-3:] else name + '.md'

    path = os.path.join(cfg.notes_path, file_name)

    if os.path.isfile(path) and not override:
        raise NoteExistsException(f'File {path} already exists')

    with open(path, 'w+') as f:
        f.write(str(note))

    return path


def list_notes(tags: List[str] = None,
               cfg: Config = None,
               **kwargs) -> List[Note]:
    if not tags:
        tags = []
    tags = list(map(lambda x: x.lower(), tags))
    if not cfg:
        raise ValueError('No config given')
    notes = []
    for f in os.listdir(cfg.notes_path):
        filename, file_extension = os.path.splitext(f)
        if file_extension == '.md':
            path = os.path.join(cfg.notes_path, f)
            note = Note.from_file(path)

            if tags:
                matches = True
                for tag in tags:
                    if tag.lower() not in note.tags:
                        matches = False

                if matches:
                    notes.append(note)
            else:
                notes.append(note)

    notes.sort(key=lambda x: x.created)
    return notes
