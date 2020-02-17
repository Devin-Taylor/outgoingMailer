from bs4 import BeautifulSoup

def read_html(filename):
    with open(filename, 'r') as fd:
        text = BeautifulSoup(fd, 'html.parser')
    return text

class Message(object):
    def __init__(self, base_html):
        with open(base_html, 'r') as fd:
            base = fd.read()
        self.email = BeautifulSoup(base, features="lxml")

    def __repr__(self):
        return str(self.email)

    def _add_field(self, text, level):
        tag = self.email.new_tag(level)
        tag.string = text
        self.email.body.append(tag)

    def add_component(self, filename, title=None, level="H3", fields=None, values=None):
        if title is not None:
            self._add_field(title, level)

        paragraph = read_html(filename)

        if fields is not None:
            if len(fields) != len(values):
                raise RuntimeError("Replacement fields and values are of different length")
            for idx, field in enumerate(fields):
                field_id = paragraph.find(id=field)
                field_id.contents[0].replace_with(values[idx])

        self.email.body.append(paragraph)

    def to_string(self):
        return str(self.email)
