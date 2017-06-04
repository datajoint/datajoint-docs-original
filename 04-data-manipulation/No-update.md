# No Update

In database programming, the **update** operation refers to changing individual attributes in a tuple within a table without replacing the entire tuple.  This allows violations of dependencies since the data computed downstream in the pipeline is not updated to reflect the change.

To preserve data integrity, DataJoint does not provide an **update** operator. Update is simply not part of the DataJoint model. All data manipulations are performed by inserting or deleting tuples from tables.

This rule applies to automated tables.  Manual and lookup tables are often edited outside DataJoint through other interfaces.  It is up to the user's discretion to allow updates there and the user must be cognizant of the fact that updates will not trigger re-computation of dependent data.