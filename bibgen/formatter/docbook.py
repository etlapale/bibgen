# DocBook formatter for citeproc-py

from xml.sax.saxutils import escape


def preformat(text):
    return escape(str(text))

class TagWrapper(str):
    tag = None
    attributes = None
    @classmethod
    def _wrap(cls, text):
        if cls.attributes:
            attrib = ' ' + ' '.join(['{}="{}"'.format(key, value)
                                     for key, value in cls.attributes.items()])
        else:
            attrib = ''
        return '<{tag}{attrib}>{text}</{tag}>'.format(tag=cls.tag,
                                                      attrib=attrib,
                                                      text=preformat(text))
    def __new__(cls, text):
        return super(TagWrapper, cls).__new__(cls, cls._wrap(text))

class Italic(TagWrapper):
    tag = 'emphasis'

class Oblique(TagWrapper):
    tag = 'emphasis'
    attributes = {'role': 'oblique'}

class Bold(TagWrapper):
    tag = 'emphasis'
    attributes = {'role': 'bold'}

class Light(TagWrapper):
    pass

class Underline(TagWrapper):
    tag = 'emphasis'
    attributes = {'role': 'underline'}

class Superscript(TagWrapper):
    tag = 'superscript'

class Subscript(TagWrapper):
    tag = 'subscript'

class SmallCaps(TagWrapper):
    tag = 'emphasis'
    attributes = {'role': 'smallcaps'}
