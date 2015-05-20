bibgen
======

Bibgen is a Python library and an associated script that allow
styled citations and bibliography generation using external
bibliographic databases. It supports databases such as BibTeX, JSON or
Mendeley_, and generates styled citations and bibliography sections
for several document types including DocBook_ and reStructuredText_,
with easy integration into Sphinx_.

Textual citations and entries in the generated bibliographies are
styled using rules found in `CSL <http://citationstyles.org/>`_
stylesheets. Thousands of those stylesheets are readily available, for
instance through the `Zotero style repository
<https://zotero.org/styles>`_.

Bibgen is available under the `Simplified BSD License`_.

Example: DocBook
----------------
Using:

.. code-block:: console

   $ bibgen --mendeley -o doc-with-bib.xml doc.xml

will replace citations such as

.. code-block:: xml

   multi-scale models <citation>Bayerl2004;Tlapale2011</citation>

by

.. code-block:: xml

   multi-scale models <citation>(<link linkend="bayerl2004">Bayerl
   &amp; Neumann 2004</link>; <link linkend="tlapale2010">Tlapale
   et al. 2010</link>)</citation>

and fill the ``<bibliography/>`` node with cooked ``<bibliomixed/>``
elements.

Documentation
-------------

.. toctree::
   :maxdepth: 2

   databases
   doctypes

Requirements
------------
In addition to a standard Python 3 installation, ``bibgen`` requires
the citeproc-py_ library to be available (support for CSL, JSON and
minimalist BibTeX databases). Currently, the git version of
citeproc-py_ avalaible on github is supported, version 0.1.0 is not.
Additionally, the following optional
libraries may be useful:

bibtexparser_
  For enhanced BibTeX support.

Download
--------
`bibgen-0.1.1.tar.xz </data/bibgen/bibgen-0.1.tar.xz>`_
(2014-09-26) Support for bibtexparser_
|
`archives </data/bibgen/>`_

`Project website <https://git.atelo.org/etlapale/bibgen>`_

You may prefer to use:

.. code-block:: console

   pip install --user bibgen

to install it with its dependencies from PyPI_.

.. _Simplified BSD License: /data/licenses/BSD
.. _AsciiDoc: http://www.asciidoc.org
.. _bibtexparser: https://github.com/sciunto-org/python-bibtexparser
.. _citeproc-py: https://github.com/brechtm/citeproc-py
.. _DocBook: http://www.docbook.org
.. _Mendeley: http://www.mendeley.com
.. _PyPI: http://pypi.python.org/pypi/bibgen
.. _reStructuredText: http://docutils.sf.net/rst.html
.. _Sphinx: http://sphinx-doc.org
.. _Zotero: http://www.zotero.org
