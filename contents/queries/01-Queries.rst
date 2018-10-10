.. progress: 12.0 50% Dimitri

.. _queries:

Query Objects
=============

**Data queries** retrieve data from the database.
A data query is formed from a **query object**, a symbolic representation of the query that does not in itself contain any actual data.
The simplest query object is an instance of a **table class**, representing the contents of an entire table.

For example, if  ``experiment.Session`` is a DataJoint table class, we can create a query object to retrieve its entire contents as follows:

.. matlab 1 start

.. code-block:: matlab

    query = experiment.Session;

.. matlab 1 end

.. python 1 start

.. code-block:: python

    query  = experiment.Session()

.. python 1 end

More generally, a query object may be formed as a **query expression** constructed by applying :ref:`operators <operators>` to other query objects.

For example, the following query retrieves information about all experiments and scans for mouse 102 (excluding experiments with no scans):

.. matlab 2 start

.. code-block:: matlab

    query = experiment.Session * experiment.Scan & 'animal_id = 102';

.. matlab 2 end

.. python 2 start

.. code-block:: python

    query = experiment.Session * experiment.Scan & 'animal_id = 102'

Note that for brevity, query operators can be applied directly to class objects rather than instance objects so that ``experiment.Session`` may be used in place of ``experiment.Session()``.

.. python 2 end

You can preview the contents of the table in Python, Jupyter Notebook, or MATLAB by simply displaying the object.
In the image below, the object ``query`` is first defined as a restriction of the table ``EEG`` by values of the attribute ``eeg_sample_rate`` greater than 1000 Hz.
When we display the object, we get a preview of the entities that will be returned by ``query``.
Note that this preview only lists a few of the entities that will be returned.
Also, the preview does not contain any data for attributes of datatype ``blob``.

.. image:: ../_static/img/query_object_preview.png

Once the desired query object is formed, the query can be executed using its :ref:`fetch` methods.
To **fetch** means to transfer the data represented by the query object from the database server into the workspace of the host language.


.. matlab 3 start

.. code-block:: matlab

    s = query.fetch()

Here fetching from the ``query`` object produces the struct array ``s`` of the queried data.

.. matlab 3 end

.. python 3 start

    s = query.fetch()

Here fetching from the ``query`` object produces the numpy record array ``s`` of the queried data.

.. python 3 end


Normalization in queries
------------------------

Query objects adhere to entity :ref:`normalization` just like the stored tables do.
The result of a query is a well-defined entity set with an readily identifiable entity class and designated primary attributes that jointly distinguish any two entities from each other.
The query :ref:`operators` are designed to keep the result normalized even in complex query expressions.
