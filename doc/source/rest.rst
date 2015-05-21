reStructuredText
================

Roles and directives
--------------------

Bibgen provides a reStructuredText_ directive to define a bibliography
database, ``bibliography``, and a directive to cite elements from that
database, ``cite``.

.. rst:directive:: bibliography

   Define a bibliography source for the current document, and print
   the list of cited items. The optional argument ``database`` can be
   used to specify a non-default database name.

   The following options are accepted:

   ``:encoding: name``
     Defines the encoding of the bibliography database.
     Defaults to ``utf-8``.

   ``:mendeley:``
     Indicates to use a Mendeley sqlite database.
     By default a BibTeX database is assume.

   ``:style: name``
     Specify the formated citation style. Defaults to ``harvard1``.
   
.. rst:role:: cite

   Insert a formatted citation to a specific bibliography item. The
   cited item will be added to the printed bibliography. Cited items
   can be inserted before the corresponding :rst:dir:`bibliography`
   directive.
		   
Command-line
------------

When using the command-line script ``bibgen``, you can either specify
the bibliography database through as a command-line argument, or by
specifying a ``bibliography`` directive.

Integration
-----------

When using bibgen as a library, you can call the
``bibgen.rst.register()`` function to register the roles and
directives of bibgen.

.. _reStructuredText: http://docutils.sf.net/rst.html
