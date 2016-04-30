import warnings

import citeproc.source
import citeproc.source.bibtex.bibtex as cbt
import citeproc.source.bibtex.bibparse as cbp

import bibtexparser
import bibtexparser.bparser
import bibtexparser.customization


class CiteProcBibTeX(cbt.BibTeX):
    '''
    BibTeX source for citeproc-py based on bibtexparser.
    '''
    def __init__(self, fp):
        self.preamble_macros = {}
        parser = bibtexparser.bparser.BibTexParser()
        parser.customization = bibtexparser.customization.convert_to_unicode
        bib_db = bibtexparser.load(fp, parser=parser)
        for entry in bib_db.entries:
            entry_type = entry['type'] if 'type' in entry \
                         else entry['ENTRYTYPE']
            entry_id = entry['id'] if 'id' in entry \
                         else entry['ID']
            bent = cbp.BibTeXEntry(entry_type, entry)
            self.add(self.create_reference(entry_id.lower(), bent))
