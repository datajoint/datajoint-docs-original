.. progress: 16.0 90% Austin

.. _query-objects:

Query Objects
=============

**Data queries** retrieve data from the database.
A data query is performed with the help of a **query object**, which is a symbolic representation of the query that does not in itself contain any actual data.
The simplest query object is an instance of a **table class**, representing the contents of an entire table.

For example, if  ``experiment.Session`` is a DataJoint table class, you can create a query object to retrieve its entire contents as follows:

.. include:: 01-Queries_lang1.rst

More generally, a query object may be formed as a **query expression** constructed by applying :ref:`operators <operators>` to other query objects.

For example, the following query retrieves information about all experiments and scans for mouse 102 (excluding experiments with no scans):


.. include:: 01-Queries_lang2.rst

You can preview the contents of the query in Python, Jupyter Notebook, or MATLAB by simply displaying the object.
In the image below, the object ``query`` is first defined as a restriction of the table ``EEG`` by values of the attribute ``eeg_sample_rate`` greater than 1000 Hz.
Displaying the object gives a preview of the entities that will be returned by ``query``.
Note that this preview only lists a few of the entities that will be returned.
Also, the preview does not contain any data for attributes of datatype ``blob``.

.. figure:: ../_static/img/query_object_preview.png
   :align: center
   :alt: query object preview

   Defining a query object and previewing the entities returned by the query.

Once the desired query object is formed, the query can be executed using its :ref:`fetch <fetch>` methods.
To **fetch** means to transfer the data represented by the query object from the database server into the workspace of the host language.



.. include:: 01-Queries_lang3.rst


Checking for returned entities
------------------------------

The preview of the query object shown above displayed only a few of the entities returned by the query but also displayed the total number of entities that would be returned.
It can be useful to know the number of entities returned by a query, or even whether a query will return any entities at all, without having to fetch all the data themselves.

.. include:: 01-Queries_lang4.rst


Normalization in queries
------------------------

Query objects adhere to entity :ref:`entity normalization <normalization>` just like the stored tables do.
The result of a query is a well-defined entity set with an readily identifiable entity class and designated primary attributes that jointly distinguish any two entities from each other.
The query :ref:`operators <operators>` are designed to keep the result normalized even in complex query expressions.
