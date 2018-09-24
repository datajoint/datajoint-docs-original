.. progress: 8.0 10% Dimitri

.. _insert:

Insert
======

The ``insert`` method of DataJoint table objects inserts entities into the table.

.. matlab 1 start

|matlab| MATLAB
---------------

In MATLAB the ``insert`` method inserts any number of entities in the form of a structure array with field attributes corresponding to the attribute names.

For example

.. code-block:: matlab

    s.username = 'alice';
    s.first_name = 'Alice';
    s.last_name = 'Cooper';
    insert(lab.Person, s)

For quick entry of multiple entities, we can take advantage of MATLAB's cell array notation:

.. code-block:: matlab

    insert(lab.Person, {
           'alice'   'Alice'   'Cooper'
           'bob'     'Bob'     'Dylan'
           'carol'   'Carol'   'Douglas'
    })

In this case, the values must match the order of the attributes in the table.
.. matlab 1 end

.. python 1 start

|python| Python
---------------

In Python there is a separate method ``insert1`` to insert one entity at a time.
The entity may have the form of a Python dictionary with key names matching the attribute names in the table.

.. code-block:: python

    lab.Person.insert1(
           dict(username='alice',
                first_name='Alice',
                last_name='Cooper'))

The entity also may take the form of a sequence of values in the same order as the attributes in the table.

.. code-block:: python

    lab.Person.insert1(['alice', 'Alice', 'Cooper'])

Additionally, the entity may be inserted as a `numpy.record <https://docs.scipy.org/doc/numpy/reference/generated/numpy.record.html#numpy.record>`_.

The ``insert`` method accepts a sequence or a generator of multiple entities and is used to insert multiple entities at once.

.. code-block:: python

    lab.Person.insert([
           ['alice',   'Alice',   'Cooper'],
           ['bob',     'Bob',     'Dylan'],
           ['carol',   'Carol',   'Douglas']])
.. python 1 end

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
In such cases, data can be :doc:`fetched <../queries/02-Fetch>` from the first table and then inserted into another table, but this results in transfers back and forth between the database and the local system.
Instead, data can be inserted from one table into another without transfers between the database and the local system using :doc:`queries <../queries/01-Queries>`.
