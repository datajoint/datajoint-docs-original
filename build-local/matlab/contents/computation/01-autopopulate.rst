.. progress: 12.0 20% Dimitri

.. _auto:

Auto-populate
=============

Tables in the initial portions of the pipeline are populated from outside the pipeline.
In subsequent steps, computations are performed automatically by the DataJoint pipeline.

Computed tables belong to one of the two auto-populated :ref:`data tiers <tiers>`: ``dj.Imported`` and ``dj.Computed``.
DataJoint does not enforce the distinction between imported and computed tables: the difference is purely semantic, a convention for developers to follow.
If populating a table requires access to external files such as raw storage that is not part of the database, the table is designated as **imported**.
Otherwise it is **computed**.

Make
----
Auto-populated tables are defined and queried exactly as other tables (See :ref:`example`).
Their data definition follows the same :ref:`definition syntax <definition-syntax>`.

For auto-populated tables, data should never be entered using :ref:`insert <insert>` directly.
Instead these tables must define the callback method ``make(self, key)``.
The ``insert`` method then can only be called on ``self`` inside this callback method.

Consider the following example:

Imagine that there is a table ``test.Image`` that contains 2D grayscale images in its ``image`` attribute.
Let us define the computed table, ``test.FilteredImage`` that filters the image in some way and saves the result in its ``filtered_image`` attribute.

The class will be defined as follows.

.. include:: 01-autopopulate_lang1.rst


The ``make`` method received one argument: the ``key`` of type ``struct`` in MATLAB and ``dict`` in Python.
The key represents the partially filled entity, usually already containing :ref:`primary key <primary-key>` attributes.

Inside the callback, three things always happen:

1. :ref:`fetch` data from tables upstream in the pipeline using the ``key`` for :ref:`restriction <restriction>`.
2. The missing attributes are computed and added to the fields already in ``key``.
3. The entire entity is inserted into ``self``.

``make`` may populate multiple entities in one call when ``key`` does not specify the entire primary key of the populated table.

Populate
--------
The inherited ``populate`` method of ``dj.Imported`` and ``dj.Computed`` automatically calls ``make`` for every key for which the auto-populated table is missing data.

The ``FilteredImage`` table can be populated as

.. include:: 01-autopopulate_lang2.rst

Note that it is not necessary to specify which data needs to be computed.
DataJoint will call ``make``, one-by-one, for every key in ``Image`` for which ``FilteredImage`` has not yet been computed.

Chains of auto-populated tables form computational pipelines in DataJoint.


.. |python| image:: ../_static/img/python-tiny.png
.. |matlab| image:: ../_static/img/matlab-tiny.png
