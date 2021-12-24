import yaml


class Config:
    def __init__(self, notes_path: str, editor: str, viewer: str):
        self.notes_path = notes_path
        self.editor = editor
        self.viewer = viewer

    @classmethod
    def from_yaml(cls, path):
        with open(path, 'r') as f:
            try:
                vals = yaml.safe_load(f)
            except yaml.YAMLError as exc:
                raise ValueError(exc)
        return Config(**vals)
