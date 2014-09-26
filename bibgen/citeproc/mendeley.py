import sqlite3
import sys

import citeproc
import citeproc.source
import citeproc.types


types = {'Book': citeproc.types.BOOK,
         'BookSection': citeproc.types.CHAPTER,
         'ConferenceProceedings': citeproc.types.PAPER_CONFERENCE,
         'JournalArticle': citeproc.types.ARTICLE_JOURNAL,
         'Report': citeproc.types.REPORT,
         'Thesis': citeproc.types.THESIS}

def parse_type(name):
    if name in types:
        return types[name]
    return None

class CiteProcMendeley(citeproc.source.BibliographySource):
    def __init__(self, database):
        # Open the sqlite database
        conn = sqlite3.connect(database)
        conn.row_factory = sqlite3.Row
        curs = conn.cursor()

        # Fetch all documents
        curs.execute('SELECT id,citationKey,type,publication,year,month,volume,issue,pages,title FROM Documents')
        docs = curs.fetchall()
        for doc in docs:
            # Check for a citation key
            if doc['citationKey'] is None:
                continue

            # Check type
            type = parse_type(doc['type'])
            if type is None:
                print('warning: skipping unknown document type ‘%s’ for %s'%(doc['type'],doc['citationKey']),
                      file=sys.stderr)
                continue
            
            # Create a date
            if doc['year'] is None:
                print('warning: skipping undated publication for', doc['citationKey'], file=sys.stderr)
                continue
            date = {'year': int(doc['year'])}
            if doc['month'] is not None:
                date['month'] = doc['month']

            # Create document metadata
            meta = {'container_title': doc['publication'],
                    'issued': citeproc.source.Date(**date),
                    'title': doc['title'],
                    'author': []
                   }

            # Other metadata
            for key in ['issue', 'volume']:
                if doc[key] is not None:
                    meta[key] = doc[key]

            # Fetch authors
            curs.execute('SELECT firstNames,lastName FROM DocumentContributors WHERE documentId=? AND contribution="DocumentAuthor"', (doc['id'],))
            authors = curs.fetchall()
            for author in authors:
                name = citeproc.source.Name(family=author['lastName'], given=author['firstNames'])
                meta['author'].append(name)

            # Parse pages
            if doc['pages'] is not None:
                pp = doc['pages'].split('-')
                if len(pp) == 1:
                    meta['page'] = citeproc.source.Pages(first=pp[0])
                else:
                    meta['page'] = citeproc.source.Pages(first=pp[0], last=pp[1])

            # Register the document
            self.add(citeproc.source.Reference(doc['citationKey'].lower(), parse_type(doc['type']), **meta))
