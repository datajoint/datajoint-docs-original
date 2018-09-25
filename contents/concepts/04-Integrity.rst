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

.. TODO: Example

Relationships
-------------

In DataJoint, the term **relationship** is used rather generally to describe the effects of particular configurations of :ref:`dependencies <dependencies>` between multiple entity sets.
A dependency of an entity set containing the death dates of mice on an entity set describing the mice themselves would obviously be a one-to-one relationship.
Other relationship types include many-to-one, one-to-many, and many-to-many.
The types of relationships between entity sets are expressed in the :ref:`ERD <erd>` of a schema.

Group integrity
---------------

**Group integrity** denotes the guarantee made by the data management process that entities composed of multiple parts always appear in their complete form.
Group integrity in DataJoint is formalized through the :ref:`master-part relationship <part>`.
