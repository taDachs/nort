import os
import re
from datetime import datetime
from typing import List, Optional

from ruamel import yaml


class SectionNotFoundException(Exception):
    pass


class Note:
    def __init__(self, name: str, content: str, tags: Optional[List[str]] = None, created=None):
        self.name = name
        self.content = content
        self.tags = tags
        if created:
            self.created = created
        else:
            self.created = datetime.now()

    def get_filename(self):
        return self.name if ".md" == self.name[-3:] else self.name + ".md"

    def get_section(self, title: str) -> str:
        lines = self.content.split("\n")
        section = ""
        started = False
        for line in lines:
            if re.match(r"#* \w*", line.strip()):
                section_title = line.replace("#", "").strip()
                if section_title == title:
                    started = True
                else:
                    started = False
            if started:
                section += line + "\n"

        if not section:
            raise SectionNotFoundException(f"Section {title} not found")

        return section

    @classmethod
    def from_file(cls, path):
        metadata = ""
        content = ""
        with open(path, "r") as f:
            line = ""
            for line in f:
                if line.strip():
                    break
            if line != "---":
                content = line + "".join(f)
            else:
                for line in f:
                    if line.strip() == "---":
                        break
                    else:
                        metadata += line
                for line in f:
                    content += line

        if metadata:
            meta = yaml.safe_load(metadata)
            if "name" not in meta:
                # for backwards compatability
                meta["name"] = meta["title"]
        else:
            name, _ = os.path.splitext(os.path.basename(path))
            meta = {"name": name, "tags": [], "created": None}

        return Note(meta["name"], content, meta["tags"], meta["created"])

    def __repr__(self):
        return f"Note({self.name}, {self.tags}, {self.created})"

    def __str__(self):
        rep = ""
        rep += "---\n"
        rep += yaml.safe_dump({"name": self.name, "tags": self.tags, "created": self.created})
        rep += "---\n"
        rep += self.content
        return rep
