BibTeX support
==============
Using BibTeX as the type of bibliography database, bibgen_ will take
as bibliography the first file with a ``.bib`` extensions it finds in
the document directory. You can also specify another bibliography
database passing it as argument after the document name:

.. code-block:: console

    $ bibgen --bibtex -o citedoc.xml doc.xml /path/to/library.bib

Parser
------

When bibtexparser_ is not available, bibgen_ will default to
citeproc-py_’s parser, which is not able to handle complex BibTeX
libraries. For instance, the following field is not correctly
recognized:

.. code-block:: tex

    author = {Escobar, Mar\'{\i}a-Jos\'{e} and […]}

Leading to a stacktrace error about ``i}a-Jos\'`` being an undefined
macro. Similarly, citeproc-py_ assumes page numbers to be made
entirely of digits, which is not the case in all journal articles, or
to have more than one page.

.. _bibgen: /code/bibgen
.. _bibtexparser: https://github.com/sciunto-org/python-bibtexparser
.. _citeproc-py: https://github.com/brechtm/citeproc-py
