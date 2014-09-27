bibgen
======
``bibgen`` is a Python script that allows styled citations and
bibliography generation using external bibliographic
databases. It supports databases such as BibTeX, JSON or
Mendeley_, and generates styled citations and bibliography
sections for several document types including DocBook_.
Textual citations and entries in the generated
bibliographies are styled using rules found in `CSL
<http://citationstyles.org/>`_ stylesheets. Thousands of those
stylesheets are readily available, for instance through the `Zotero
style repository <https://zotero.org/styles>`_.

Most of the code is available as a library to allows
better integration in your Python code. ``bibgen`` is a free software
released under the `Apache License 2.0`_.
See the work of :cite:`Tlapale2010` or :cite:`Bayerl2004`.

Requirements
------------
In addition to a standard Python 3 installation, ``bibgen`` requires
the citeproc-py_ library to be available (support for CSL, JSON and
minimalist BibTeX databases). Additionally, the following optional
libraries may be useful:

bibtexparser_
  For enhanced BibTeX support.

Download
--------
`bibgen-0.1.1.tar.xz </data/bibgen/bibgen-0.1.tar.xz>`_
(2014-09-26) Support for bibtexparser_.

`archives </data/bibgen/>`_

You may prefer to use::

    pip install --user bibgen

to install it with its dependencies from PyPI_.

.. _Apache License 2.0: /data/licenses/APACHE
.. _AsciiDoc: http://www.asciidoc.org
.. _bibtexparser: https://github.com/sciunto-org/python-bibtexparser
.. _citeproc-py: https://github.com/brechtm/citeproc-py
.. _DocBook: http://www.docbook.org
.. _Mendeley: http://www.mendeley.com
.. _PyPI: http://pypi.python.org/pypi/bibgen
.. _reStructuredText: http://docutils.sf.net/rst.html
.. _Zotero: http://www.zotero.org
