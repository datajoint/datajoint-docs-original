.. progress: 12.0 25% Austin

Creating Schemas
================

Relational data model
---------------------
DataJoint organizes data using the *Relational Data Model*.
This means that all data are stored in collections of simple tables.
The relationships between tables comprise the structure of a data pipeline.

See also :doc:`../concepts/2-terminology`

Classes represent tables
------------------------
To make it easy to work with tables in MATLAB and Python, DataJoint programs create a separate class for each table.
Computer programmers refer to this concept as `object-relational mapping <https://en.wikipedia.org/wiki/Object-relational_mapping>`_.
For example, the class ``experiment.Subject`` in MATLAB or Python may correspond to the table called ``subject`` on the database server.
Users never need to see the database directly; they only interact with data in the database by creating and interacting with DataJoint classes.

Schemas
-------
On the database server, related tables are grouped into a named collection called a **schema**.
This grouping organizes the data and allows control of user access.
Depending on the complexity of the data, a database server may have many schemas each containing a subset of tables, or a single schema may contain every table, in the simplest cases.
Schemas outline the structure of a data pipeline by specifying the directional relationships between tables.
DataJoint reflects this organization by associating each DataJoint class with its corresponding schema.
Tables are defined within the context of a schema, so we must create a schema before we can create any tables.

.. include:: 01-Creating-Schemas_lang1.rst

Working with existing data
--------------------------
What if the database schema already exists?
For example, what if we created the schema in Python but want to access the data from MATLAB or vice versa?
No problem.
Follow the same process for creating the schema and specify the existing schema name.
We will show how to work with existing tables later.


