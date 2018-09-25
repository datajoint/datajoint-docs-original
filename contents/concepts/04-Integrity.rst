.. progress: 18 0% Dimitri

.. _entity_integrity:

Entity integrity
----------------

In a proper relational design, each table represents a collection of discrete real-world entities of some kind.
**Entity integrity** is the guarantee made by the data management process that entities from the real world are reliably and uniquely represented in the database system.
Entity integrity states that the data management process must prevent duplicate representations or misidentification of entities.
DataJoint enforces entity integrity through the use of :ref:`primary keys <primary-key>`.

Entity integrity breaks down when a process allows data pertaining to the same real-world entity to be entered into the database system multiple times.
For example, a school database system may use unique ID numbers to distinguish students.
Suppose the system automatically generates an ID number each time a student record is entered into the database without checking whether a record already exists for that student.
Such a system violates entity integrity, because the same student may be assigned multiple ID numbers.
The ID numbers succeed in uniquely identifying each student record but fail to do so for the actual students.

Referential integrity
---------------------

**Referential integrity** is the guarantee made by the data management process that related data across the database remain present, correctly associated, and mutually consistent.
Guaranteeing referential integrity means enforcing the constraint that no entity can exist in the database without all the other entities on which it depends.
Referential integrity cannot exist without entity integrity: references to entity cannot be validated if the identity of the entity itself is not guaranteed.



Relationships
-------------

Group integrity
---------------
