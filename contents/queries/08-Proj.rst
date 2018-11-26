.. progress: 12.0 60% Austin

.. _proj:

Proj
====

The ``proj`` operator is used to select attributes (columns) from a table, to rename them, or to create new calculated attributes.

Simple projection
-----------------

The simple projection selects a subset of attributes of the original table.
However, the primary key attributes are always included.

Using the :ref:`example schema <query-example>`, let table ``department`` have attributes **dept**, *dept_name*, *dept_address*, and *dept_phone*.
The primary key attribute is in bold.

Then ``department.proj()`` will have attribute **dept**.

``department.proj('dept')`` will have attribute **dept**.

``department.proj('dept_name', 'dept_phone')`` will have attributes **dept**, *dept_name*, and *dept_phone*.

Renaming
--------

In addition to selecting attributes, ``proj`` can rename them.
Any attribute can be renamed, including primary key attributes.

.. include:: 08-Proj_lang1.rst


For example, let table ``tab`` have attributes **mouse**, **session**, *session_date*, *stimulus*, and *behavior*.
The primary key attributes are in bold.

Then

.. include:: 08-Proj_lang2.rst


will have attributes **animal**, **session**, and *stimulus*.

Renaming is often used to control the outcome of a :ref:`join <join>`.
For example, let ``tab`` have attributes **slice**, and **cell**.
Then ``tab * tab`` will simply yield ``tab``.
However,

.. include:: 08-Proj_lang3.rst


yields all ordered pairs of all cells in each slice.

Calculations
------------

In addition to selecting or renaming attributes, ``proj`` can compute new attributes from existing ones.

For example, let ``tab`` have attributes ``mouse``, ``scan``, ``surface_z``, and ``scan_z``.
To obtain the new attribute ``depth`` computed as ``scan_z - surface_z`` and then to restrict to
``depth > 500``:

.. include:: 08-Proj_lang4.rst


Calculations are passed to SQL and are not parsed by DataJoint.
For available functions, you may refer to the `MySQL documentation <https://dev.mysql.com/doc/refman/5.7/en/functions.html>`_.
