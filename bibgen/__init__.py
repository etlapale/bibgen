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

import os
import os.path
import pathlib

docbook_ns = 'http://docbook.org/ns/docbook'


def default_mendeley_database():
    '''
    Search for a default Mendeley sqlite database.
    '''
    # Linux
    dirs = [os.path.expanduser('~/.local/share/data/Mendeley Ltd./Mendeley Desktop')]
    # Windows Vista/7 (untested)
    if 'LOCALAPPDATA' in os.environ:
        dirs.append(os.path.join(os.environ('LOCALAPPDATA'),
                                 'Mendeley Ltd.', 'Mendeley Desktop'))
    # Windows XP (untested)
    dirs.append(os.path.join(os.path.expanduser('~'),
                             'Local Settings', 'Application Data',
                             'Mendeley Ltd.', 'Mendeley Desktop'))
    # MacOS X
    dirs.append(os.path.join(os.path.expanduser('~'),
                             'Library', 'Application Support',
                             'Mendeley Desktop'))
    
    for d in dirs:
      for path in pathlib.Path(d).glob('*@www.mendeley.com.sqlite'):
          return str(path)
    return None

def default_bibtex_database(doc):
    for d in [os.path.dirname(doc)]:
        for path in pathlib.Path(d).glob('*.bib'):
            return str(path)
    return None
