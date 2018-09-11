.. progress: 8.0 75% Dimitri

Composite Attributes
====================

.. important::
  This page serves as feature specification.
  The feature will be included in an upcoming release.

In the relational model, data are structured such that entities represented in one table all share the same set of attributes.
This introduces clarity and enables predictable queries.
In datasets with many categories of entities with different sets of attributes, relational designs result in large numbers of tables.
Sometimes it is conventient to deviate from the relational data model and to allow different sets of attributes in each entity.
This can already be accomplished by storing structures of dicts inside blob fields.
However, blob fields are opaque to queries: their contents cannot be used in searches.

DataJoint introduces the datatype ``composite`` to allow storing objects with their own collections of attributes.

For example, the following :doc:`table definition <03-Table-Definition>` has a composite attribute ``stimulus``.

.. code-block:: text

    # Recording
    rec   :  int    # recording id
    ----
    filepath  :  varchar(255)   #  filepath to the recording data
    stimulus : composite  #  parameters of the stimulus


Inserts
-------
To insert data into a composite attribute, use a ``struct`` in MATLAB or a ``dict`` in Python.

For example,

|matlab| MATLAB

.. code-block:: matlab

    insert(test.Recording, struct('rec', 1, 'filepath', '/my/data/path', 'stimulus', struct('contrast', 0.3, 'luminance', 3.5)))

|python| Python

.. code-block:: python

   test.Recording().insert1(dict(rec=1, filepath='/my/data/path', 'stimulus'=dict(contrast=0.3, luminance=3.5)))

Queries
-------
The main purpose of composite attributes is to allow their use in restrictions.
This is done by using the ``attribute.field`` notation.

For example, the following restriction selects all recordings for which the stimulus is defined and exceeds 0.5.

.. code-block:: python

    Recording() & 'stimlus.comtrast > 0.5'



.. warning::
   The composite datatype relies on JSON support by the database server.
   Latest versions of MySQL and MariaDB provide JSON support, but Amazon's own Aurora DB  does not.
   We hope to use Aurora DB and hope that it will soon add JSON support.


.. |python| image:: ../_static/img/python-tiny.png
.. |matlab| image:: ../_static/img/matlab-tiny.png
