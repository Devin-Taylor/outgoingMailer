from typing import List

from bs4 import BeautifulSoup


def read_html(filename: str):
    with open(filename, 'r') as fd:
        text = BeautifulSoup(fd, 'html.parser')
    return text

class Message(object):
    def __init__(self, base_html: str, start_id: str = None):
        with open(base_html, 'r') as fd:
            base = fd.read()
        self.email = BeautifulSoup(base, features="lxml")
        if start_id is not None:
            self.start_tag = self.email.find(id=start_id)
        else:
            self.start_tag = self.email.body

    def __repr__(self):
        return str(self.email)

    def _add_field(self, text: str, level: str):
        tag = self.email.new_tag(level)
        tag.string = text
        self.start_tag.append(tag)

    def add_component(self, filename: str, title: str = None, level: str = "H4", fields: List[str] = None, values: List[str] = None):
        if title is not None:
            self._add_field(title, level)

        paragraph = read_html(filename)

        if fields is not None:
            if len(fields) != len(values):
                raise RuntimeError("Replacement fields and values are of different length")
            for idx, field in enumerate(fields):
                field_id = paragraph.find(id=field)
                field_id.contents[0].replace_with(values[idx])

        self.start_tag.append(paragraph)

    def to_string(self):
        return str(self.email)
