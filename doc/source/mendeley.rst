Mendeley support
================
To specify that you want bibgen_ to use Mendeley_ as a bibliography
database, passe the ``--mendeley`` option as command line argument.

The content of your Mendeley_ bibliography is accessed directly through
the sqlite backup on your local computer, as found by the
``default_mendeley_database()`` function.

Each document of the Mendeley database must have a *Citation Key*
field to be citable through bibgen_. In Mendeley you can view and
modify citation keys by having a look into the *Details* tab,
typically on the right when you select a document. If it is not
shown, you can go to *Tools*/*Options*/*Document Details* and enable it
for the different document type it is needed.

.. _bibgen: /code/bibgen
.. _Mendeley: http://www.mendeley.com
