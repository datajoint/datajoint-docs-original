.. progress: 12.0 25%  Dimitri

.. _proj:

Proj
====

The ``proj`` operator is used to select attributes (columns) from a table, to rename them, or to create new calculated attributes.

Simple projection
-----------------

The simple projection selects a subset of attributes of the original table.
However, the primary key attributes are always included.

For example, let table ``tab`` have attributes **``mouse``**, **``session``**, ``session_date``, ``stimulus``, and ``behavior``.
The primary key attributes are in bold.

Then ``tab.proj()`` will have attributes **``mouse``** and **``session``**.

``tab.proj('mouse')`` will have attributes **``mouse``** and **``session``**.

``tab.proj('behavior', 'stimulus')`` will have attributes **``mouse``**, **``session``**, ``behavior``, and ``stimulus``.

Renaming
--------

In addition to selecting attributes, ``proj`` can rename them.
Any attribute can be renamed, including primary key attributes.


.. include: 07-Proj_lang1.rst

For example, let table ``tab`` have attributes **``mouse``**, **``session``**, ``session_date``, ``stimulus``, and ``behavior``.
The primary key attributes are in bold.

Then


.. include: 07-Proj_lang2.rst

will have attributes **``animal``**, **``session``**, and ``stimulus``.

Renaming is often used to control the outcome of a :ref:`join`.
For example, let ``tab`` have attributes **``slice``**, and **``cell``**.
Then ``tab * tab`` will simply yield ``tab``.
However,


.. include: 07-Proj_lang3.rst

yields all ordered pairs of all cells in each slice.

Calculations
------------

In addition to selecting or renaming attributes, ``proj`` can compute new attributes from existing ones.

For example, let ``tab`` have attributes **``mouse``**, **``scan``**, ``surface_z``, and ``scan_z``.
To obtain the new attribute ``depth`` computed as ``scan_z - surface_z`` and then to restrict to
``depth > 500``:


.. include: 07-Proj_lang4.rst

Calculations are passed to SQL and are not parsed by DataJoint.
For available functions, you may refer to the `MySQL documentation <https://dev.mysql.com/doc/refman/5.7/en/functions.html>`_.
