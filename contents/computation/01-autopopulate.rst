.. progress: 12.0 20% Dimitri

.. _auto:

Auto-populate
=============

Auto-populated tables are used to define, execute, and coordinate computations in a DataJoint pipeline.

Tables in the initial portions of the pipeline are populated from outside the pipeline.
In subsequent steps, computations are performed automatically by the DataJoint pipeline in auto-populated tables.

Computed tables belong to one of the two auto-populated :ref:`data tiers <tiers>`: ``dj.Imported`` and ``dj.Computed``.
DataJoint does not enforce the distinction between imported and computed tables: the difference is purely semantic, a convention for developers to follow.
If populating a table requires access to external files such as raw storage that is not part of the database, the table is designated as **imported**.
Otherwise it is **computed**.

Auto-populated tables are defined and queried exactly as other tables.
(See :ref:`example`.)
Their data definition follows the same :ref:`definition syntax <definition-syntax>`.

.. _make:

Make
----
For auto-populated tables, data should never be entered using :ref:`insert <insert>` directly.
Instead these tables must define the callback method ``make(self, key)``.
The ``insert`` method then can only be called on ``self`` inside this callback method.

Imagine that there is a table ``test.Image`` that contains 2D grayscale images in its ``image`` attribute.
Let us define the computed table, ``test.FilteredImage`` that filters the image in some way and saves the result in its ``filtered_image`` attribute.

The class will be defined as follows.


.. include:: 01-autopopulate_lang1.rst

The ``make`` method received one argument: the ``key`` of type ``struct`` in MATLAB and ``dict`` in Python.
The key represents the partially filled entity, usually already containing the :ref:`primary key <primary-key>` attributes of the key source.

The ``make`` callback does three things:

1. :ref:`Fetches <fetch>` data from tables upstream in the pipeline using the ``key`` for :ref:`restriction <restriction>`.
2. Computes and adds any missing attributes to the fields already in ``key``.
3. Inserts the entire entity into ``self``.

``make`` may populate multiple entities in one call when ``key`` does not specify the entire primary key of the populated table.

Populate
--------
The inherited ``populate`` method of ``dj.Imported`` and ``dj.Computed`` automatically calls ``make`` for every key for which the auto-populated table is missing data.

The ``FilteredImage`` table can be populated as

.. include:: 01-autopopulate_lang2.rst

Note that it is not necessary to specify which data needs to be computed.
DataJoint will call ``make``, one-by-one, for every key in ``Image`` for which ``FilteredImage`` has not yet been computed.

Chains of auto-populated tables form computational pipelines in DataJoint.

Populate options
----------------

.. include:: 01-autopopulate_lang3.rst

Progress
--------

.. include:: 01-autopopulate_lang4.rst
