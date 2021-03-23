.. progress: 4 100% Dimitri

.. _update:

Cautious Update
===============

In database programming, the **update** operation refers to modifying the values of individual attributes in an entity within a table without replacing the entire entity.
Such an in-place update mechanism is not part of DataJoint's data manipulation model, because it circumvents data :ref:`dependency constraints <referential-integrity>`.

This is not to say that data cannot be changed once they are part of a pipeline.
In DataJoint, data is changed by replacing entire entities rather than by updating the values of their attributes.
The process of deleting existing entities and inserting new entities with corrected values ensures the :ref:`integrity <integrity>` of the data throughout the pipeline.

This approach applies specifically to automated tables (see :ref:`auto`).
However, manual tables are often edited outside DataJoint through other interfaces.
It is up to the user's discretion to allow updates in manual tables, and the user must be cognizant of the fact that updates will not trigger re-computation of dependent data.

Usage
-----

For some cases, it becomes necessary to deliberately correct existing values where a user has chosen to accept the above responsibility despite the caution.

The ``update1`` method accomplishes this if the record already exists. Note that updates to primary key values are not allowed.

The method should only be used to fix problems, and not as part of a regular workflow. When updating an entry, make sure that any information stored in dependent tables that depends on the update values is properly updated as well.

Examples
--------

.. include:: 1-Update_lang1.rst