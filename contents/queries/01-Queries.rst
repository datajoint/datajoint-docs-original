.. progress: 12.0 50% Dimitri

.. _queries:

Query Objects
=============

**Data queries** retrieve data from the database.

A data query is formed from  a **query object**, a symbolic representation of the query that represents the query but does not yet contain the actual data.

The simplest query object is an instance of a **table class**, representing the entire table.

For example, if  ``experiment.Session`` is a DataJoint table class, we can create a query object to retrieve its entire contents as follows:

.. matlab 1 start

.. code:: matlab

    query = experiment.Session;

.. matlab 1 end

.. python 1 start

.. code:: python

    query  = experiment.Session()

.. python 1 end

More generally, a query object may be formed as a **table expression** constructed by applying :ref:`operators` to instances of tables classes or to other table expressions.

For example, the following table contains information about all experiments and scans for mouse 102 (excluding experiments with no scans):

.. matlab 2 start

.. code:: matlab

    query = experiment.Session * experiment.Scan & 'animal_id = 102';

.. matlab 2 end

.. python 2 start

.. code:: python

    tab = experiment.Session * experiment.Scan & 'animal_id = 102'

Note that for brevity, query operators can be applied directly to class objects rather than instances objects.

.. python 2 end

You can preview the contents of the table in Python, Jupyter

Notebook, or MATLAB by simply display the object:

<< FIGURE >>

Once the desired query object is formed, the query can be executed using its ref:`fetch` methods.

To "fetch" means to transfer the data represented by the query object from the database server into the workspace of the host language.


Normalization in queries
------------------------

Query objects adhere to entity :ref:`normalization` just like the stored tables do.
The result of a query is a well-defined entity set with an readily identifiable entity class and designated primary attributes that jointly distinguish any two entities from each other.
The query :ref:`operators` are designed to keep the result normalized even in complex query expressions.
