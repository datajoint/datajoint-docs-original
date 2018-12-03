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
Tables are defined within a schema, so a schema must be created before the creation of any tables.


.. include:: 01-Creating-Schemas_lang1.rst

Working with existing data
~~~~~~~~~~~~~~~~~~~~~~~~~~

See the chapter :ref:`existing` for how to work with data in existing pipelines, including accessing a pipeline from one language when the pipeline was developed using another.

.. |matlab| image:: ../_static/img/matlab-tiny.png
.. |python| image:: ../_static/img/python-tiny.png
