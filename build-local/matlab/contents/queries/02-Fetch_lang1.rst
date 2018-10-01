
MATLAB
------

DataJoint for MATLAB provides three distinct fetch methods: ``fetch``, ``fetch1``, and ``fetchn``.
The three methods differ by the type and number of their returned variables.

``query.fetch`` returns the result in the form of an *n* ⨉ 1  `struct array <https://www.mathworks.com/help/matlab/ref/struct.html>`_ where *n*.

``query.fetch1`` and ``query.fetchn`` split the result into separate output arguments, one for each attribute of the query.

The types of the variables returned by ``fetch1`` and ``fetchn`` depend on the :ref:`datatypes` of the attributes.
``query.fetchn`` will enclose any attributes of  char and blob types in  `cell arrays <https://www.mathworks.com/help/matlab/cell-arrays.html>`_ whereas ``query.fetch1`` will unpack them.

MATLAB has two alternative forms of invoking a method on an object: using the dot notation or passing the object as the first argument.
The following two notations produce an equivalent result:

.. code:: matlab

    result = query.fetch(query, 'attr1')
    result = fetch(query, 'attr1')

However, the dot syntax only works when the query object is already assigned to a variable.
The second syntax is more commonly used to avoid extra variables.

For example, the two methods below are equivalent although the second method creates an extra variable.

.. code:: matlab

    # Method 1
    result = fetch(experiment.Session, '*');

    # Method 2
    query = experiment.Session;
    result = query.fetch()


Fetch the primary key
~~~~~~~~~~~~~~~~~~~~~

Without any arguments, the ``fetch`` method retrieves the primary key values of the table in the form of a single column ``struct``.
The attribute names become the fieldnames of the ``struct``.

.. code:: matlab

    keys = query.fetch;
    keys = fetch(experiment.Session & experiment.Scan);

Note that MATLAB allows calling functions without the parentheses ``()``.


Fetch entire query
~~~~~~~~~~~~~~~~~~

With a single-quoted asterisk (``'*'``) as the input argument, the ``fetch`` command retrieves the entire result as a struct array.

.. code:: matlab

    data = query.fetch('*');

    data = fetch(experiment.Session & experiment.Scan, '*');

In some cases, the amount of data returned by fetch can be quite large.
When ``query`` is a table object rather than a query expression, ``query.sizeOnDisk()`` reports the estimated size of the entire table.
It can be used to assess whether running ``query.fetch('*')`` would be wise.
Please note that it is only currently possible to query the size of entire tables stored directly in the database .

As separate variables
~~~~~~~~~~~~~~~~~~~~~

The ``fetch1`` and ``fetchn`` methods are used to retrieve each attribute into a separate variable.
We need two different methods to tell MATLAB whether the result should be in array or scalar form; for numerical fields it does not matter (because scalars are still matrices in matlab) but non-uniform collections of values must be enclosed in cell arrays.

``query.fetch1`` is used when ``query``  contains exactly one entity, otherwise ``fetch1`` will raise an error.

``query.fetchn`` returns an arbitrary number of elements with character arrays and blobs returned in the form of cell arrays, even when  ``query`` happens to contain a single entity.

.. code:: matlab

    % when tab has exactly one entity:
    [name, img] = query.fetch1('name', 'image');

    % when tab has any number of entities:
    [names, imgs] = query.fetchn('name', 'image');


Obtaining the primary key along with individual values
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
It is often convenient to know the primary key values corresponding to attribute values retrieved by ``fetchn``.
This can be done by adding a special input argument indicating the request and another output argument to receive the key values:

.. code:: matlab

    % retrieve names, images, and corresponding primary key values:
    [names, imgs, keys] = query.fetchn('name', 'image', 'KEY');

The resulting value of ``keys`` will be a column array of type ``struct``.
This mechanism is only implemented for ``fetchn``.

Rename and calculate
~~~~~~~~~~~~~~~~~~~~

In DataJoint for MATLAB, all ``fetch`` methods have all the same capability as the :ref:`proj` operator.
For example, renaming an attribute can be accomplished using the syntax below.

.. code:: matlab

    [names, BMIs] = query.fetchn('name', 'weight/height/height -> bmi');

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
