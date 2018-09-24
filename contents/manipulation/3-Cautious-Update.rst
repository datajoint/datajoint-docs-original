.. progress: 6 20% Dimitri

.. _update:

Cautious Update
===============

In database programming, the **update** operation refers to modifying the values of individual attributes in an entity within a table without replacing the entire entity.

Updates are not part of DataJoint's data manipulation model, because updates allow going around data dependency constraints.
In DataJoint data are manipulated by inserting or deleting entities in tables.

This approach applies to automated tables (See :ref:`auto`).

However, manual tables are often edited outside DataJoint through other interfaces.
It is up to the user's discretion to allow updates there, and the user must be cognizant of the fact that updates will not trigger re-computation of dependent data.
