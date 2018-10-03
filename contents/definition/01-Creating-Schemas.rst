.. progress: 8.0 50% Austin

.. _schema:

Creating Schemas
================

Schemas
~~~~~~~
On the database server, related tables are grouped into a named collection called a **schema**.
This grouping organizes the data and allows control of user access.
A database server may contain multiple schemas each containing a subset of the tables.
A single pipeline may comprise multiple schemas.
Tables are defined within a schema, so we must create a schema before we can create any tables.


.. include:: 01-Creating-Schemas_lang1.rst

Working with existing data
~~~~~~~~~~~~~~~~~~~~~~~~~~
What if the database schema already exists?
For example, what if we created the schema in Python but want to access the data from MATLAB or vice versa?
Follow the same process for creating the schema and specify the existing schema name.
We will show how to work with existing tables later.

.. |matlab| image:: ../_static/img/matlab-tiny.png
.. |python| image:: ../_static/img/python-tiny.png
