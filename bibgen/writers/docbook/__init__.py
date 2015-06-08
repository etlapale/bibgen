# -*- coding: utf-8; -*-
#
# bibgen/writers/docbook/__init__.py — Adds math support to DocBook writer
#
# Copyright © 2015 Émilien Tlapale
# Licensed under the Simplified BSD License


from __future__ import absolute_import, division, print_function

from .oliverr import Writer as OllieWriter
from .oliverr import DocBookTranslator as OllieTranslator


class Writer(OllieWriter):
    def translate(self):
        visitor = DocBookTranslator(self.document)
        self.document.walkabout(visitor)
        self.output = visitor.astext()

        
class DocBookTranslator(OllieTranslator):
    def __init__(self, document):
        OllieTranslator.__init__(self, document)
        
    def visit_math(self, node):
        self.body.append('<inlineequation>\n')

    def depart_math(self, node):
        self.body.append('</inlineequation>\n')

    def visit_container(self, node):
        pass

    def depart_container(self, node):
        pass
        
    def visit_math_block(self, node):
        self.body.append('<equation>\n')

    def depart_math_block(self, node):
        self.body.append('</equation>\n')
