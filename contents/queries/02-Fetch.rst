.. progress: 6.0  20% Dimitri

.. _fetch:

Fetch
=====

Data queries in DataJoint comprise two distinct steps:

1. Construct the table or :ref:`operators` ``tab`` to represent the required data.
2. Fetch the data from ``tab`` into the workspace of the host language -- described in this section.

Fetch works somewhat differently between MATLAB and Python.

Note that entities returned by ``fetch`` methods are not guaranteed to be sorted in any particular order unless specifically requested.
Furthermore, the order is not guaranteed to be the same in any two queries, and the contents of two identical queries may change between two sequential invocations unless they are wrapped in a transaction.
Therefore, if you wish to fetch matching pairs of attributes, do so in one ``fetch`` call.

.. matlab 1 start

MATLAB
------

DataJoint for MATLAB provides three distinct ``fetch`` methods, each covering a separate use case.
The three methods differ by the type and number of their returned variables.
The method ``fetch`` returns a single column `structure array <https://www.mathworks.com/help/matlab/ref/struct.html>`_ or ``struct``.
The methods ``fetch1`` and ``fetchn`` return a separate variable for the values of each attribute.
The types of the variables returned by ``fetch1`` and ``fetchn`` depend on the :ref:`datatypes` of the attributes.
Attributes containing ``varchar`` or ``blob`` data will be returned as `cell arrays <https://www.mathworks.com/help/matlab/cell-arrays.html>`_ by ``fetchn``.

All ``fetch`` methods can be called directly on a base table or table expression ``tab``, such as ``tab.fetch()``.
Base tables and table expressions can also be passed as the first argument of a ``fetch`` method, as in ``fetch(tab)``.
However the dot syntax does not apply when fetching from a table expression directly, without first assigning that table expression to a variable.
In such cases, the expression must be passed as the first argument of the ``fetch`` call, as in ``fetch(tab1 & tab2)`` for tables ``tab1`` and ``tab2``.

Fetch the primary key
~~~~~~~~~~~~~~~~~~~~~

Without any arguments, the ``fetch`` method retrieves the primary key values of the table in the form of a single column ``struct``.
The attribute names become the fieldnames of the ``struct``.

.. code:: matlab

    keys = tab.fetch; % for table or expression tab

    keys = fetch(tab1 & tab2); % for a table expression on tables tab1 and tab2

Fetch entire table
~~~~~~~~~~~~~~~~~~

With a single-quoted asterisk (``'*'``) as the input argument, the ``fetch`` command retrieves all data from ``tab`` as a ``struct``.

.. code:: matlab

    data = tab.fetch('*'); % for table or expression tab

    data = fetch(tab1 & tab2, '*'); % for a table expression on tables tab1 and tab2

In some cases, the amount of data returned by fetch can be quite large.
When ``tab`` is a table, it can be useful to call the ``tab.sizeOnDisk()`` function to determine if running a bare fetch would be wise.
Please note that it is only currently possible to query the size of entire tables stored directly in the database at this time.
It is only possible to call ``sizeOnDisk()`` on a base table.

As separate variables
~~~~~~~~~~~~~~~~~~~~~

The ``fetch1`` and ``fetchn`` methods are used to retrieve each attribute into a separate variable.

``tab.fetch1`` is used when ``tab`` is known to contain exactly one entity.
If ``tab.fetch1`` is called when ``tab`` contains more than one entity or zero entities, an error will occur.
As mentioned above, strings and blobs returned by ``fetch1`` are retrieved unwrapped.

``tab.fetchn`` is used for an arbitrary number of entities in ``tab``.
In this case, strings and blobs are returned in the form of cell arrays, even if ``tab.fetchn`` happens to return only a single entity.

.. code:: matlab

    % when tab has exactly one entity:
    [name, img] = tab.fetch1('name', 'image');

    % when tab has any number of entities:
    [names, imgs] = tab.fetchn('name', 'image');

    % when table expression has exactly one entity:
    [name, img] = fetch1(tab1 & tab2, 'name', 'image');

    % when table expression has any number of entities:
    [names, imgs] = fetchn(tab1 & tab2, 'name', 'image');


Obtaining the primary key along with individual values
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is often convenient to know the primary key values corresponding to attribute values retrieved by ``fetchn``.
This can be done by adding a special input argument indicating the request and another output argument to receive the key values:

.. code:: matlab

    % retrieve names, images, and corresponding primary key values:
    [names, imgs, keys] = fetchn(tab, 'name', 'image', 'KEY');

The resulting value of ``keys`` will be a column array of type ``struct``.
This mechanism is only implemented for ``fetchn``.

Rename and calculate
~~~~~~~~~~~~~~~~~~~~

In DataJoint for MATLAB, all ``fetch`` methods have all the same capability as the :ref:`proj` operator.
For example, renaming an attribute can be accomplished using the syntax below.

.. code:: matlab

    % for table tab:
    [names, BMIs] = tab.fetchn('name', 'weight/height/height -> bmi');

See :ref:`proj` for an in-depth description of projection.

Sorting and limiting the results
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To sort the result, add the additional ``ORDER BY`` argument in ``fetch`` and ``fetchn`` methods as the last argument.

.. code:: matlab

    % retrieve field `notes` from experiment sessions
    % performed by Alice, sorted by session date
    notes = fetchn(experiment.Session & 'operator="alice"', 'note', ...
         'ORDER BY session_date');

The ORDER BY argument is passed directly to SQL and follows the same syntax as the `ORDER BY clause <https://dev.mysql.com/doc/refman/5.7/en/order-by-optimization.html>`_

Similarly, the LIMIT and OFFSET clauses can be used to limit the result to a subset of entities.
For example, to return the top most recent sessions, one could do the following:

.. code:: matlab

    s = fetch(experiment.Session, '*', 'ORDER BY session_date DESC LIMIT 5')

The limit clause is passed directly to SQL and follows the same `rules <https://dev.mysql.com/doc/refman/5.7/en/select.html>`_
.. matlab 1 end

.. python 1 start

Python
------

Entire table
~~~~~~~~~~~~

The following statement retrieves the entire table as a NumPy `recarray <https://docs.scipy.org/doc/numpy/reference/generated/numpy.recarray.html>`_.

.. code:: python

    data = tab.fetch()

To retrieve the data as a list of ``dict``:

.. code:: python

    data = tab.fetch(as_dict=True)

Furthermore, the ``fetch`` object can be used as a generator for loops:

.. code:: python

    for row in tab.fetch:
       # row is a dict

In some cases, the amount of data returned by fetch can be quite large; in these cases it can be useful to use the ``size_on_disk`` attribute to determine if running a bare fetch would be wise.
Please note that it is only currently possible to query the size of entire tables stored directly in the database at this time.

As separate variables
~~~~~~~~~~~~~~~~~~~~~

::

    name, img = tab.fetch1('name', 'image')  # when tab has exactly one entity
    name, img = tab.fetch('name', 'image')  # [name, ...] [image, ...] otherwise

Primary key values
~~~~~~~~~~~~~~~~~~

::

    keydict = tab.fetch1("KEY")  # single key dict when tab has exactly one entity
    keylist = tab.fetch("KEY")  # list of key dictionaries [{}, ...] otherwise

Usage with Pandas
~~~~~~~~~~~~~~~~~

The ``pandas`` `library <http://pandas.pydata.org/>`_ is a popular library for data analysis in Python which can easily be used with DataJoint query results.
Since the records returned by ``fetch()`` are contained within a ``numpy.recarray``, they can be easily converted to ``pandas.DataFrame`` objects by passing them into the ``pandas.DataFrame`` constructor.
For example:

::

    import pandas as pd
    frame = pd.DataFrame(tab.fetch())

.. python 1 end
