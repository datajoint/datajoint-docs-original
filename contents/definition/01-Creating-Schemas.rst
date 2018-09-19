.. progress: 12.0 25% Austin

Creating Schemas
================

Schemas
~~~~~~~
On the database server, related tables are grouped into a named collection called a **schema**.
This grouping organizes the data and allows control of user access.
Depending on the complexity of the data, a database server may have many schemas each containing a subset of tables, or a single schema may contain every table, in the simplest cases.
Schemas outline the structure of a data pipeline by specifying the directional relationships between tables.
DataJoint reflects this organization by associating each DataJoint class with its corresponding schema.
Tables are defined within the context of a schema, so we must create a schema before we can create any tables.

.. matlab 1 start

|matlab| MATLAB
---------------------------
A schema can be created in MATLAB either manually or automatically through the ``dj.createSchema`` script.
While ``dj.createSchema`` simplifies the process, the manual approach yields a better understanding of what actually takes place, so both approaches are listed below.

Manual
^^^^^^^^^^^^
**Step 1.**  Create the database schema

Use the following command to create a new schema on the database server:

.. code-block:: matlab

    query(dj.conn, 'CREATE SCHEMA `alice_experiment`')

Note that you must have create privileges for the schema name pattern (as described in :doc:`../admin/1-hosting`).
It is a common practice to grant all privileges to users for schemas that begin with the username, in addition to some shared schemas.
Thus the user ``alice`` would be able to perform any work in any schema that begins with ``alice_``.

**Step 2.**  Create the MATLAB package

DataJoint for MATLAB organizes schemas as MATLAB **packages**.
If you are not familiar with packages, please review:

* `How to work with MATLAB packages <https://www.mathworks.com/help/matlab/matlab_oop/scoping-classes-with-packages.html>`_
* `How to manage MATLAB's search paths <https://www.mathworks.com/help/matlab/search-path.html>`_

In your project directory, create the package folder, which must begin with a ``+`` sign.
For example, for the schema called ``experiment``, you would create the folder ``+experiment``.
Make sure that your project directory (the parent directory of your package folder) is added to the MATLAB search path.

**Step 3.**  Associate the package with the database schema

In this step, we tell DataJoint that all classes in the package folder ``+experiment`` will work with tables in the database schema ``alice_experiment``.
Each package in MATLAB corresponds to exactly one schema.
In some special cases, multiple packages may all relate to a single database schema, but in most cases there will be a one-to-one relationship between packages and schemas.

In the ``+experiment`` folder, create the file ``getSchema.m`` with the following contents:

.. code-block:: matlab

    function obj = getSchema
    persistent OBJ
    if isempty(OBJ)
        OBJ = dj.Schema(dj.conn, 'experiment', 'alice_experiment');
    end
    obj = OBJ;
    end

This function returns a persistent object of type ``dj.Schema``, establishing the link between the ``experiment`` package in MATLAB and the schema ``alice_experiment`` on the database server.

Automatic
^^^^^^^^^^^^^

Alternatively, you can execute

.. code-block:: matlab

    >> dj.createSchema

This automated script will walk you through the steps 1--3 above and will create the schema, the package folder, and the ``getSchema`` function in that folder.
.. matlab 1 end

.. python 1 start

|python| Python
----------------

Create a new schema using the ``dj.schema`` function:

.. code-block:: python

    import datajoint as dj
    schema = dj.schema('alice_experiment')

This statement creates the database schema ``alice_experiment`` on the server.

The returned object ``schema`` will then serve as a decorator for DataJoint classes, as described in :doc:`02-Creating-Tables`.

It is a common practice to have a separate Python module for each schema.
Therefore, each such module has only one ``dj.schema`` object defined and is usually named ``schema``.

The ``dj.schema`` constructor can take a number of optional parameters after the schema name.

- ``context`` - Dictionary for looking up foreign key references.
  Defaults to ``None`` to use local context.
- ``connection`` - Specifies the DataJoint connection object.
  Defaults to ``dj.conn()``.
- ``create_schema`` - When ``False``, the schema object will not create a schema on the database and will raise an error if one does not already exist.
  Defaults to ``True``.
- ``create_tables`` - When ``False``, the schema object will not create tables on the database and will raise errors when accessing missing tables.
  Defaults to ``True``.
  
.. python 1 end

Working with existing data
~~~~~~~~~~~~~~~~~~~~~~~~~~
What if the database schema already exists?
For example, what if we created the schema in Python but want to access the data from MATLAB or vice versa?
Follow the same process for creating the schema and specify the existing schema name.
We will show how to work with existing tables later.

.. |matlab| image:: ../_static/img/matlab-tiny.png
.. |python| image:: ../_static/img/python-tiny.png
