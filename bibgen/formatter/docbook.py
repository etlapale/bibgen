# DocBook formatter for citeproc-py

from citeproc.formatter.html import TagWrapper, preformat

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
