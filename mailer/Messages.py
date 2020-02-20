from typing import Dict

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

    def add_component(self, filename: str, title: str, replacements: Dict[str, Dict[str, str]], applicant: Dict[str, str], level: str = "H3"):
        if title is not None:
            self._add_field(title, level)

        paragraph = read_html(filename)

        if replacements is not None:
            for field, vals in replacements.items():
                field_id = paragraph.find(id=field)
                if field_id is not None:
                    if vals.get('value') is not None:
                        field_id.contents[0].replace_with(str(applicant.get(vals.get('value'))))
                    if vals.get('params') is not None:
                        for param, rep in vals.get('params').items():
                            field_id[param] = str(applicant.get(rep))

        self.start_tag.append(paragraph)

    def to_string(self) -> str:
        return str(self.email)
