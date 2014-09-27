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

import docutils.core
import docutils.nodes
import docutils.parsers.rst
import docutils.parsers.rst.roles


def cite_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    docutils.parsers.rst.roles.set_classes(options)
    ref = 'http://emilien.tlapale.com/bibgen'
    node = docutils.nodes.reference(rawtext, 'Citation number 42', refuri=ref,
                                    **options)
    return [node], []

def register():
    docutils.parsers.rst.roles.register_canonical_role('cite', cite_role)

def process_file(source, **kwds):
    str = docutils.core.publish_string(source, **kwds)
    return str

#cite_role.options = …
#cite_role.content = …
