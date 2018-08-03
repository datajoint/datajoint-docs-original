Proj
====

The ``proj`` operator is used to select attributes (columns) from a
relation, to rename them, or to create new calculated attributes.

Simple projection
-----------------

The simple projection selects a subset of attributes of the original
relation. However, the primary key attributes are always included.

For example, let relation ``rel`` have attributes **``mouse``**,
**``session``**, ``session_date``, ``stimulus``, and ``behavior``. The
primary key attributes are in bold.

Then ``rel.proj()`` will have attributes **``mouse``** and
**``session``**.

``rel.proj('mouse')`` will have attributes **``mouse``** and
**``session``**.

``rel.proj('behavior', 'stimulus')`` will have attributes **``mouse``**,
**``session``**, ``behavior``, and ``stimulus``.

Renaming
--------

In addition to selecting attributes, ``proj`` can rename them. Any
attribute can be renamed, including primary key attributes.

In Python, this is done using keyword arguments:
``rel.proj(new_attr='old_attr')``

In MATLAB, renaming is done using a string:
``rel('old_attr->new_attr')``.

For example, let relation ``rel`` have attributes **``mouse``**,
**``session``**, ``session_date``, ``stimulus``, and ``behavior``. The
primary key attributes are in bold.

Then

.. code:: python

    # python
    rel.proj(animal='mouse', 'stimulus')

.. code:: matlab

    % matlab 
    rel.proj('mouse->animal', 'stimulus')

will have attributes **``animal``**, **``session``**, and ``stimulus``.

Renaming is often used to control the outcome of a [[join]]. For
example, let ``rel`` have attributes **``slice``**, and **``cell``**.
Then ``rel * rel`` will simply yield ``rel``. However,

.. code:: python

    # python
    rel * rel.proj(other='cell')

.. code:: matlab

    % matlab
    rel * rel.proj('cell->other')

yields all ordered pairs of all cells in each slice.

Calculations
------------

In addition to selecting or renaming attributes, ``proj`` can compute
new attributes from existing ones.

For example, let ``rel`` have attributes **``mouse``**, **``scan``**,
``surface_z``, and ``scan_z`` and we need to obtain the new attribute
``depth`` computed as ``scan_z - surface_z`` and then restrict to
``depth > 500``:

.. code:: python

    # python
    rel.proj(depth='scan_z-surface_z') & 'depth > 500'

.. code:: matlab

    % matlab 
    rel.proj('scan_z-surface_z -> depth') & 'depth > 500'

Calculations are passed to SQL and are not parsed by DataJoint. For
available function, you may refer to MySQL documentation
https://dev.mysql.com/doc/refman/5.7/en/functions.html.
