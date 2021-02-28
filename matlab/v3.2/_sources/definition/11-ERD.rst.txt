.. progress: 24.0 10% Dimitri

.. _erd:

ERD
===

ERD stands for **entity relationship diagram**.
Objects of type ``dj.ERD`` allow visualizing portions of the data pipeline in graphical form.
Tables are depicted as nodes and :ref:`dependencies <dependencies>` as directed edges between them.
The `draw` method plots the graph.

Diagram notation
----------------
Consider the following ERD

.. image:: ../_static/img/mp-erd.png

DataJoint uses the following conventions:

* Tables are indicated as nodes in the graph.
  The corresponding class name is indicated by each node.
* :ref:`Data tiers <tiers>` are indicated as colors and symbols: Lookup=gray asterisk, Manual=green square, Imported=blue circle, Computed=red star, Part=black dot.
  The names of :ref:`part tables <master-part>` are indicated in a smaller font.
* :ref:`dependencies` are indicated as edges in the graph and always directed downward, forming a **directed acyclic graph**.
* Foreign keys contained within the primary key are indicated as solid lines.
  This means that the referenced table becomes part of the primary key of the dependent table.
* Foreign keys that are outside the primary key are indicated by dashed lines.
* If the primary key of the dependent table has no other attributes besides the foreign key, the foreign key is a thick solid line, indicating a 1:{0,1} relationship.
* Foreign keys made without renaming the foreign key attributes are in black whereas foreign keys that rename the attributes are indicated in red.

Diagramming an entire schema
----------------------------

.. include:: 11-ERD_lang1.rst


Initializing with a single table
++++++++++++++++++++++++++++++++

A `dj.ERD` object can be initialized with a single table.


.. include:: 11-ERD_lang2.rst

A single node makes a rather boring graph but ERDs can be added together or subtracted from each other using graph algebra.

Adding ERDs together
++++++++++++++++++++

However two graphs can be added, resulting in new graph containing the union of the sets of nodes from the two original graphs.
The corresponding foreign keys will be automatically


.. include:: 11-ERD_lang3.rst

Expanding ERDs upstream and downstream
++++++++++++++++++++++++++++++++++++++

Adding a number to an ERD object adds nodes downstream in the pipeline while subtracting a number from ERD object adds nodes upstream in the pipeline.

Examples:


.. include:: 11-ERD_lang4.rst

.. |python| image:: ../_static/img/python-tiny.png
.. |matlab| image:: ../_static/img/matlab-tiny.png
