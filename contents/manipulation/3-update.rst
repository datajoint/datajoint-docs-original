Cautious update
===============

In database programming, the **update** operation refers to modifying the values of individual attributes in a tuple within a table without replacing the entire tuple.  

Updates are not part of DataJoint's data manipulation model because updates allow going around data dependencies constraint.  In DataJoint data are manipulated by inserting or deleting tuples in tables.

This approach applies to automated tables (See :doc:`../computation/01-autopopulate`).

However, manual tables are often edited outside DataJoint through other interfaces.  It is up to the user's discretion to allow updates there and the user must be cognizant of the fact that updates will not trigger re-computation of dependent data.
