#! /usr/bin/env python3

from setuptools import setup

setup(name='bibgen',
      version='0.1.1',
      description='A citation and bibliography generator',
      long_description='''bibgen is a Python script that allows styled
      citations and bibliography generation using external
      bibliographic databases. It supports databases such as BibTeX,
      JSON or Mendeley, and generates styled citations and
      bibliography sections for several document types including
      DocBook. Textual citations and entries in the generated
      bibliographies are styled using rules found in CSL
      stylesheets. Thousands of those stylesheets are readily
      available, for instance through the Zotero style repository.''',
      author='Émilien Tlapale',
      author_email='emilien@tlapale.com',
      url='http://emilien.tlapale.com/code/bibgen',
      packages=['bibgen',
                'bibgen.citeproc'],
      scripts=['bin/bibgen'],
      install_requires = ['citeproc-py'],
      extras_require = {
        'enhanced_bibtex':  ['bibtexparser']
      },
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: Apache Software License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Topic :: Software Development :: Documentation',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Text Processing',
          'Topic :: Text Processing :: Markup :: XML',
      ],
     )
