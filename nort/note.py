from typing import List


class Note:
    def __init__(self, name: str, content: str, tags: List[str] = None):
        self.name = name
        self.content = content
        self.tags = tags

    @classmethod
    def from_file(cls, path):
        with open(path, 'r') as f:
            lines = f.readlines()

        started = False
        for line in lines:
            if line.strip() == '%%%' and not started:
                started = True
            elif line.strip() == '%%%' and started:
                break

            if not started:
                continue

            if 'name: ' in line:
                name = line.split(' ')[1].strip()

            if 'tags: ' in line:
                tags = line.split(' ')[1][1:-2].split(',')

        return Note(name, '', tags)

    def __repr__(self):
        rep = ''
        rep += '%%%\n'
        rep += f'tags: [{",".join(self.tags)}]\n'
        rep += f'name: {self.name}\n'
        rep += '%%%\n'
        rep += self.content
        return rep
