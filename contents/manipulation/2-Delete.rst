.. progress: 6.0 10% Dimitri

.. _delete:

Delete
======

The ``delete`` (Python) and ``del`` (MATLAB) method deletes entities from a table and all dependent entries in dependent tables.
Delete is often used in conjunction with the :ref:`restriction <restriction>` operator to define the subset of entities to delete.
Delete is performed as an atomic transaction so that partial deletes never occur.

Examples
--------

.. include:: 2-Delete_lang1.rst

Deleting from part tables
-------------------------

.. include:: 2-Delete_lang2.rst
