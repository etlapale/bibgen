DocBook support
===============
Citations
---------
bibgen_ is able to process <`citation/`_> elements in a DocBook
document. The simplest way to use it is to set the content of the
element to be the cited entry key. For instance, having a bibliography
entry whose citation is set to ``Bayerl2004``, you can insert a
DocBook citation with:

.. code-block:: xml

  <citation>Bayerl2004</citation>

If you want to refer to multiple entries in a single citation,
separate them with semi-columns:

.. code-block:: xml

  <citation>Bayerl2004;Tlapale2010</citation>

You could also specify another citation separator such as a comma
using the ``-t`` or ``--citation-separator`` command line argument,
or passing it as a ``citation_separator=','`` argument to
``process_dom()`` in direct API calls.

Links
-----
For each citation, bibgen_ will fill the ``<citation/>`` elements
with textual content including one of multiple <`link/`_> elements
pointing to entries in the generated bibliography. Typically, a filled
in citation would look like:

.. code-block:: xml

    <citation>
    (<link linkend="bayerl2004">Bayerl &amp; Neumann 2004</link>;
    <link linkend="tlapale2010">Tlapale et al. 2010</link>)
    </citation>

with spacing added for clarity. The link targets are formed from the
citation keys. You can customize them by specifying a prefix, using
the ``-p`` or ``--link-prefix`` command line argument, or passing a
function as ``link_format`` argument to ``process_dom()``:

.. code-block:: python

    bibgen.process_dom(…, link_format=lambda key: 'bib-'+key.lower())

Bibliography
------------
Each entry in the bibliography is a cooked citation, a <`bibliomixed/`_>
element, that follows the current CSL stylesheet, with an ``xml:id``
attribute matching the ``linkend`` format inside the citations:

.. code-block:: xml

    <bibliomixed xml:id="bib-tlapale2010">
    Tlapale, É. et al., 2010.
    Modelling the dynamics of motion integration […]
    </bibliomixed>

Depending on the stylesheet, certain elements such as the journal name
may have additional formatting elements. Typically <`emphasis/`_> with
optional `bold` or `oblique` roles.
    
.. _bibgen: /code/bibgen
.. _bibliomixed/: http://docbook.org/tdg51/en/html/bibliomixed.html
.. _emphasis/: http://docbook.org/tdg51/en/html/emphasis.html
.. _citation/: http://docbook.org/tdg51/en/html/citation.html
.. _link/: http://docbook.org/tdg51/en/html/link.html
