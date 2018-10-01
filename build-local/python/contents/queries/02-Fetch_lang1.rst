
Python
------

Entire table
~~~~~~~~~~~~

The following statement retrieves the entire table as a NumPy `recarray <https://docs.scipy.org/doc/numpy/reference/generated/numpy.recarray.html>`_.

.. code:: python

    data = query.fetch()

To retrieve the data as a list of ``dict``:

.. code:: python

    data = query.fetch(as_dict=True)

Furthermore, the ``query`` object can be used as a generator for loops:

.. code:: python

    for row in query:
       # row is a dict
       print(row)

In some cases, the amount of data returned by fetch can be quite large; in these cases it can be useful to use the ``size_on_disk`` attribute to determine if running a bare fetch would be wise.
Please note that it is only currently possible to query the size of entire tables stored directly in the database at this time.

As separate variables
~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    name, img = query.fetch1('name', 'image')  # when tab has exactly one entity
    name, img = query.fetch('name', 'image')  # [name, ...] [image, ...]

Primary key values
~~~~~~~~~~~~~~~~~~

.. code:: python

    keydict = tab.fetch1("KEY")  # single key dict when tab has exactly one entity
    keylist = tab.fetch("KEY")  # list of key dictionaries [{}, ...]

Usage with Pandas
~~~~~~~~~~~~~~~~~

The ``pandas`` `library <http://pandas.pydata.org/>`_ is a popular library for data analysis in Python which can easily be used with DataJoint query results.
Since the records returned by ``fetch()`` are contained within a ``numpy.recarray``, they can be easily converted to ``pandas.DataFrame`` objects by passing them into the ``pandas.DataFrame`` constructor.
For example:

.. code:: python

    import pandas as pd
    frame = pd.DataFrame(tab.fetch())

