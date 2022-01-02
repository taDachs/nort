import importlib.util
import os
import inspect
from abc import ABC, abstractmethod
from typing import List
from datetime import date, datetime

from .note import Note
from .config import Config

substitutions = {
    '[[DATE]]': date.today().strftime('%d.%m.%Y'),
    '[[TIME]]': datetime.now().strftime('%H:%M'),
}


def substitute_placeholders(s: str) -> str:
    for key, val in substitutions.items():
        s = s.replace(key, val)

    return s


class Template(ABC):
    cfg = None

    @classmethod
    def set_config(cls, cfg: Config):
        cls.cfg = cfg

    @abstractmethod
    def get_name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_tags(self) -> List[str]:
        raise NotImplementedError

    @abstractmethod
    def get_content(self) -> str:
        raise NotImplementedError

    def to_note(self) -> Note:
        name = substitute_placeholders(self.get_name())
        tags = list(set(map(substitute_placeholders, self.get_tags())))
        content = substitute_placeholders(self.get_content())
        return Note(name=name, tags=tags, content=content)


def template_by_name(name: str, cfg: Config) -> Template:
    path = cfg.template_path
    if os.path.isfile(path):
        spec = importlib.util.spec_from_file_location('user_templates', path)
        foo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(foo)
        clsmembers = inspect.getmembers(foo, inspect.isclass)
        try:
            _, cls = next(
                filter(
                    lambda x: x[0].lower() == name.lower() and issubclass(
                        x[1], Template), clsmembers))
        except StopIteration:
            raise ValueError(f'{name} is not a valid template name')
        Template.set_config(cfg)
        return cls()
    else:
        raise ValueError('No template file exists')
