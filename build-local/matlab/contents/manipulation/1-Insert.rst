.. progress: 8.0 10% Dimitri

.. _insert:

Insert
======

The ``insert`` method of DataJoint table objects inserts entities into the table.

.. include:: 1-Insert_lang1.rst


Batched inserts
---------------
Inserting a set of entities in a single ``insert`` differs from inserting the same set of entities one-by-one in a ``for`` loop in two ways:

1. Network overhead is reduced.
   Network overhead can be tens of milliseconds per query.
   Inserting 1000 entities in a single ``insert`` call may save a few seconds over inserting them individually.
2. The insert is performed as an all-or-nothing transaction.
   If even one insert fails because it violates any constraint, then none of the entities in the set are inserted.

However, inserting too many entities in a single query may run against buffer size or packet size limits of the database server.
Due to these limitations, performing inserts of very large numbers of entities should be broken up into moderately sized batches, such as a few hundred at a time.

.. |python| image:: ../_static/img/python-tiny.png
.. |matlab| image:: ../_static/img/matlab-tiny.png

Server-side inserts
-------------------

Data inserted into a table often come from other tables already present on the database server.
In such cases, data can be :ref:`fetched <fetch>` from the first table and then inserted into another table, but this results in transfers back and forth between the database and the local system.
Instead, data can be inserted from one table into another without transfers between the database and the local system using :ref:`queries <queries>`.
