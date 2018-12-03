.. progress: 12.0 30% Dimitri

.. _master-part:

Master-Part Relationship
========================

Often an entity in one table is inseparably associated with a group of entities in another, forming a **master-part** relationship.
The master-part relationship ensures that all parts of a complex representation appear together or not at all.
This has become one of the most powerful data integrity principles in DataJoint.

As an example, imagine segmenting an image to identify regions of interest.
The resulting segmentation is inseparable from the ROIs that it produces.
In this case, the two tables might be called ``Segmentation`` and ``Segmentation.ROI``.

.. include:: 04-master-part_lang1.rst

Populating
----------

Master-part relationships can form in any data tier, but DataJoint observes them more strictly for auto-populated tables.
To populate both the master ``Segmentation`` and the part ``Segmentation.ROI``, it is sufficient to call the ``populate`` method of the master:

.. include:: 04-master-part_lang2.rst

Note that the entities in the master and the matching entities in the part are inserted within a single ``make`` call of the master, which means that they are a processed inside a single transactions: either all are inserted and committed or the entire transaction is rolled back.
This ensures that partial results never appear in the database.

For example, imagine that a segmentation is performed, but an error occurs halfway through inserting the results.
If this situation were allowed to persist, then it might appear that 20 ROIs were detected where 45 had actually been found.

Deleting
--------

To delete from a master-part pair, one should never delete from the part tables directly.
The only valid method to delete from a part table is to delete the master.
This has been an unenforced rule, but upcoming versions of DataJoint will prohibit direct deletes from the master table.
DataJoint's :ref:`delete <delete>` operation is also enclosed in a transaction.

Together, the rules of master-part relationships ensure a key aspect of data integrity: results of computations involving multiple components and steps appear in their entirety or not at all.

.. |python| image:: ../_static/img/python-tiny.png
.. |matlab| image:: ../_static/img/matlab-tiny.png

Multiple parts
--------------

The master-part relationship cannot be chained or nested.
DataJoint does not allow part tables of other part tables per se.
However, it is common to have multiple part tables that depend on each other.
For example:

.. include:: 04-master-part_lang3.rst
