# Copyright © 2014  Émilien Tlapale
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import citeproc

import docutils.core
import docutils.nodes
import docutils.parsers.rst
import docutils.parsers.rst.roles


class CitationTransform(docutils.transforms.Transform):
    '''
    Docutils transform generating text for the registered citations.
    Citations are registered during a first pass occuring at node
    construction, but their text may need all the citations to be
    generated first, for instance for numbering.
    '''

    default_priority = 700

    def apply(self):
        raw_cit = self.startnode.details['raw_citation']
        cit = self.startnode.details['citation']
        biblio = self.startnode.details['biblio']

        def warn(cit_item):
            print('warning: citation reference not found for', cit_item.key)
        cit_txt = biblio.cite(cit,warn)

        node = docutils.nodes.reference(raw_cit, cit_txt,
                                        refuri='http://emilien.tlapale.com')
        self.startnode.replace_self(node)

def cite_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    docutils.parsers.rst.roles.set_classes(options)

    # Create a citation
    biblio = inliner.document.settings.biblio
    keys = text.split(';')
    def mkitem(key):
        return citeproc.CitationItem(key)
    cit = citeproc.Citation([mkitem(key) for key in keys])
    biblio.register(cit)

    # Create a pending transform to generate the reference
    # A transform is necessary to get a second pass, after numbering
    # and other first pass citation process has been performed
    pending = docutils.nodes.pending(CitationTransform)
    pending.details['raw_citation'] = text
    pending.details['citation'] = cit
    pending.details['biblio'] = biblio
    inliner.document.note_pending(pending)

    # Container serving as position marker for the reference
    node = docutils.nodes.container()
    node.setup_child(pending)
    node += pending

    return node, []

def register():
    docutils.parsers.rst.roles.register_canonical_role('cite', cite_role)

def process_file(source, biblio, **kwds):
    if 'settings_overrides' in kwds:
        so = kwds['settings_overrides']
    else:
        so = {}
        kwds['settings_overrides'] = so
    so['biblio'] = biblio
    str = docutils.core.publish_string(source, **kwds)
    return str
