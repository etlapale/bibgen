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
        parser = bibtexparser.bparser.BibTexParser()
        parser.customization = bibtexparser.customization.convert_to_unicode
        bib_db = bibtexparser.load(fp, parser=parser)
        for entry in bib_db.entries:
            bent = cbp.BibTeXEntry(entry['type'], entry)
            self.add(self.create_reference(entry['id'].lower(), bent))

    # This functions is copy/pasted/modified from citeproc-py
    def _bibtex_to_csl(self, bibtex_entry):
        csl_dict = {}
        for field, value in bibtex_entry.items():
            try:
                csl_field = self.fields[field]
            except KeyError:
                if field not in ('year', 'month', 'filename'):
                    warnings.warn("Unsupported BibTeX field '{}'".format(field))
                continue
            if field in ('number', 'volume'):
                try:
                    value = int(value)
                except ValueError:
                    pass
            elif field == 'pages':
                if value.endswith('+'):
                    value = citeproc.source.Pages(first=value[:-1])
                else:
                    fl = value.replace(' ', '').split('--')
                    if len(fl) > 1:
                        value = citeproc.source.Pages(first=fl[0], last=fl[1])
                    else:
                        value = citeproc.source.Pages(first=fl[0])
            elif field in ('author', 'editor'):
                value = [name for name in self._parse_author(value)]
            else:
                try:
                    value = self._parse_title(value)
                except TypeError:
                    value = str(value)
            csl_dict[csl_field] = value
        return csl_dict

