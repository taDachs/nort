import os

from ruamel import yaml


class Config:
    def __init__(self, notes_path: str, editor: str, viewer: str,
                 template_path: str = None):
        self.notes_path = os.path.expanduser(notes_path)
        self.editor = editor
        self.viewer = viewer
        self.template_path = template_path

    @classmethod
    def from_yaml(cls, path):
        with open(path, 'r') as f:
            try:
                vals = yaml.safe_load(f)
            except yaml.YAMLError as exc:
                raise ValueError(exc)
        return Config(**vals)
