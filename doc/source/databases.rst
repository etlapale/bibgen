Bibliographic databases
=======================

Currently, BibTex, JSON and Mendeley bibliographic databases are
supported by bibgen.

Zotero_ support may be added in the future but is impeded by the fact
that Zotero locks its local sqlite database, only allowing cloudy
access to it. This could be bypassed, for instance by setting
toggling ``extensions.zotero.dbLockExclusive`` or by writting yet
another browser plugin to provide the missing API.

.. toctree::
   :maxdepth: 3

   bibtex
   json
   mendeley

.. _Zotero: http://www.zotero.org
