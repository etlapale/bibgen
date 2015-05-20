reStructuredText
================

Roles and directives
--------------------

Bibgen offers a ``cite`` directive to insert single of multiple
citations in reStructuredText_ documents.

A ``bibliography`` directive can also be used to insert
bibliographies.

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
