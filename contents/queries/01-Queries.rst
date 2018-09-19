.. progress: 12.0 20% Dimitri

Query Basics
============

DataJoint allows manipulating and previewing data in the form of
**table objects** without retrieving any of the data into the workspace
of the host language.

In the simplest case, ``tab`` is a **simple table** representing data
on the database. For example, we can instantiate the
``experiment.Session`` table as

.. code:: matlab

    % matlab
    tab = experiment.Session;       % in MATLAB, constructors do not require parentheses ()

.. code:: python

    # MATLAB or Python
    tab = experiment.Session

More generally, ``tab`` may be a **table expression** constructed as an
expression using :doc:`query operators <03-Operators>`.

For example, the following table contains information about all
experiments and scans for mouse 102 (excluding experiments with no
scans):

.. code:: matlab

    % matlab
    tab = experiment.Session * experiment.Scan & 'animal_id = 102';

.. code:: python

    # Python or MATLAB
    tab = experiment.Session * experiment.Scan & 'animal_id = 102'

In Python, querying via attribute dictionaries is also permitted:

::

    # Python
    tab = experiment.Session * experiment.Scan & {'animal_id': 102}

You can preview the contents of the table in Python, Jupyter
Notebook, or MATLAB by simply display the object:

<< FIGURE >>

To "fetch" means to transfer the data represented by the table object on the database server
into the workspace of the host language.

All queries have the form ``tab.fetch()`` where ``tab`` is a table object and ``fetch`` is one of several variants of fetch methods, which
are described in :doc:`02-Fetch`.
