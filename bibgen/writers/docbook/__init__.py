# -*- coding: utf-8; -*-
#
# bibgen/writers/docbook/__init__.py — Adds math support to DocBook writer
#
# Copyright © 2015 Émilien Tlapale
# Licensed under the Simplified BSD License


from __future__ import absolute_import, division, print_function

import docutils.nodes as nodes

from .oliverr import Writer as OllieWriter
from .oliverr import DocBookTranslator as OllieTranslator


DOCBOOK_NS = 'http://docbook.org/ns/docbook'
DOCBOOK_VERSION = '5.0'


class Writer(OllieWriter):
    def translate(self):
        visitor = DocBookTranslator(self.document)
        self.document.walkabout(visitor)
        self.output = visitor.astext()

        
class DocBookTranslator(OllieTranslator):
    def __init__(self, document):
        OllieTranslator.__init__(self, document)
        self.doc_header = [
            self.XML_DECL % (document.settings.output_encoding,),
            '<%s xmlns="%s" version="%s">\n' \
                % (self.doctype, DOCBOOK_NS, DOCBOOK_VERSION)
        ]
        self.doc_footer = [
            '</%s>\n' % self.doctype
        ]

        self.ctxs = []

    def push_ctx(self):
        self.ctxs.append(self.body)
        self.body = []

    def pop_ctx(self):
        self.body = self.ctxs.pop()

    def astext(self):
        return ''.join(self.doc_header
                       + ['<info>\n'] + self.docinfo + ['</info>\n']
                       + self.body
                       + self.doc_footer)

    def visit_docinfo(self, node):
        docinfo = ['<title>%s</title>\n' % self.title]
        for child in node:
            if isinstance(child, nodes.date):
                docinfo.append('<date>%s</date>\n' % child.astext())
            elif isinstance(child, nodes.authors):
                for a in child:
                    docinfo.append('<author><personname>%s</personname></author>\n' % a.astext())
            else:
                print('unknown docinfo node: ', child)
        self.docinfo = docinfo
        raise nodes.SkipChildren

    def visit_topic(self, node):
        if 'abstract' in node.get('classes'):
            self.push_ctx()
            self.body.append(self.starttag(node, 'abstract'))
            self.context.append('abstract')
        else:
            OllieTranslator.visit_topic(self, node)

    def depart_topic(self, node):
        OllieTranslator.depart_topic(self, node)
        if 'abstract' in node.get('classes'):
            self.docinfo.append(''.join(self.body))
            self.pop_ctx()
        
    def visit_math(self, node):
        self.body.append('<inlineequation>\n')

    def depart_math(self, node):
        self.body.append('</inlineequation>\n')

    def visit_container(self, node):
        pass

    def depart_container(self, node):
        self.body.append('\n')
        
    def visit_math_block(self, node):
        self.body.append('<equation>\n')

    def depart_math_block(self, node):
        self.body.append('</equation>\n')

    def visit_section(self, node):
        if 'bibliography' in node.get('classes'):
            self.body.append('\n<bibliography>\n')
        else:
            return OllieTranslator.visit_section(self, node)
        
    def depart_section(self, node):
        if 'bibliography' in node.get('classes'):
            self.body.append('</bibliography>\n')
        else:
            return OllieTranslator.depart_section(self, node)
        
    def visit_paragraph(self, node):
        # Cooked bibliography entry
        if 'bibentry' in node.get('classes'):
            self.body.append('<bibliomixed>')
        # Normal paragraph
        else:
            return OllieTranslator.visit_paragraph(self, node)

    def depart_paragraph(self, node):
        # Cooked bibliography entry
        if 'bibentry' in node.get('classes'):
            self.body.append('</bibliomixed>\n')
        # Normal paragraph
        else:
            return OllieTranslator.depart_paragraph(self, node)
