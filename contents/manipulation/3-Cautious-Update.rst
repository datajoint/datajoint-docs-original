.. progress: 4 100% Dimitri

.. _update:

Cautious Update
===============

In database programming, the **update** operation refers to modifying the values of individual attributes in an entity within a table without replacing the entire entity.
Such an in-place update mechanism is not part of DataJoint's data manipulation model, because it circumvents data :ref:`dependency constraints <referential-integrity>`.

This is not to say that data cannot be changed once they are part of a pipeline.
In DataJoint, data are changed by replacing entire entities rather than by updating the values of their attributes.
The process of deleting existing entities and inserting new entities with corrected values ensures the :ref:`integrity <integrity>` of the data throughout the pipeline.

This approach applies specifically to automated tables (see :ref:`auto`).
However, manual tables are often edited outside DataJoint through other interfaces.
It is up to the user's discretion to allow updates in manual tables, and the user must be cognizant of the fact that updates will not trigger re-computation of dependent data.
