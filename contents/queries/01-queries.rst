.. progress: 12.0 20% Dimitri

Query Basics
============

DataJoint allows manipulating and previewing data in the form of
**table expressions** without retrieving any of the data into the workspace
of the host language.

In the simplest case, ``tab`` is a **simple table** representing a table of data
in the database. For example, we can instantiate the
``experiment.Session`` table as

.. code:: matlab

    % matlab
    tab = experiment.Session;       % in Matlab, constructors do not require parentheses ()

.. code:: python

    # matlab or python
    tab = experiment.Session()

More generally, ``tab`` may be a **table expression** constructed as an
expression using :doc:`query operators <03-operators>`.

For example, the following table contains information about all
experiments and scans for mouse 102 (excluding experiments with no
scans):

.. code:: matlab

    % matlab
    tab = experiment.Session * experiment.Scan & 'animal_id = 102';

.. code:: python

    # python or matlab
    tab = experiment.Session() * experiment.Scan() & 'animal_id = 102'

In python, querying via attribute dictionaries is also permitted:

::

    # python
    tab = experiment.Session() * experiment.Scan() & {'animal_id': 102}

You can preview the contents of the table in Python, Jupyter
Notebook, or MATLAB by simply display the object:

<< FIGURE >>

To "fetch" means to transfer the data represented by the table on the database server
into the workspace of the host language.

All queries have the form ``tab.fetch()`` where ``tab`` is a table and ``fetch`` is one of several variants of fetch methods, which
are described in :doc:`02-fetch`.
