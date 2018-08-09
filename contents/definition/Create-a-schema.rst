===============
Create a schema
===============

Relational Data Model
---------------------
DataJoint organizes data using the *Relational Data Model*.  This means that all data are stored in collections of simple tables or, in mathematical lingo, *relations*. 

See also :doc:`../concepts/2-terminology`
 
Classes represent tables
------------------------
To make it easy to work with tables in MATLAB and Python, DataJoint programs create a separate class for each table.  Computer programmers refer to this concept as `object-relational mapping <https://en.wikipedia.org/wiki/Object-relational_mapping>`_.  For example, the class ``experiment.Subject`` in MATLAB or Python may correspond to the table called ``experiment.subject`` on the database server.
Users never need to see the database directly and interact with data in the database by creating and interacting with DataJoint classes.   

Schemas
-------
On the database server, related tables are grouped into a named collection called **database** or **schema**.  This allows organizing the data and controlling access by users.  Therefore, we need a way of associating DataJoint classes with their schema.  This way we may address tables as ``schema.TableClassName``.  Before we create any tables, we must create a schema.

|matlab| MATLAB
---------------------------
There are two equivalent ways to create a schema in MATLAB: manual and automated using the ``dj.createSchema`` script.  While ``dj.createSchema`` simplifies the process, the manual approach yields a better understand of what actually takes place.  Therefore, we list both approaches:

Manually
^^^^^^^^^^^^
**Step 1.**  Create the database

Use the following command to create a new database on the server:

.. code-block:: matlab

    query(dj.conn, 'CREATE SCHEMA `alice_experiment`')

Note that you must have create privileges for the database name pattern (as described in [Database hosting]).  It is a common practice to grant all privileges to users to databases that begin with the username in addition to some shared databases.  Thus the user ``alice`` would be able to perform any work in any database that begins with ``alice_``.

**Step 2.**  Create the MATLAB package

DataJoint for matlab organizes schemas as MATLAB packages. If you are not familiar with them, please review

* how to work with MATLAB **packages**: https://www.mathworks.com/help/matlab/matlab_oop/scoping-classes-with-packages.html 
* how to manage MATLAB's **search paths** work: https://www.mathworks.com/help/matlab/search-path.html.

In your project directory, create the package folder, which must begin with a ``+`` sign.  For example, for the schema called ``experiment``, you would create the folder ``+experiment``.  Make sure that your project directory (the parent directory of your package folder) is added to the MATLAB search path. 

**Step 3.**  Associate the package with the database schema

In this step, we will tell DataJoint that all classes in the package folder ``+experiment`` will work with tables in the database schema ``alice_experiment``. 

In the ``+experiment`` folder, create the file ``getSchema.m`` with the following contents:

.. code-block:: matlab

    function obj = getSchema
    persistent OBJ
    if isempty(OBJ)
        OBJ = dj.Schema(dj.conn, 'experiment', 'alice_experiment');
    end
    obj = OBJ;
    end

This function returns a persistent object of type ``dj.Schema``, establishing the link between the ``experiment`` package in MATLAB and the database ``alice_experiment`` on the database server.

Automatically
^^^^^^^^^^^^^

Alternatively, you can execute 

.. code-block:: matlab

    >> dj.createSchema

This automated script will walk you through the steps 1--3 above and will create the database, the package folder, and the ``getSchema`` function in that folder.

|python| Python
----------------

Create a new schema using the ``dj.schema`` function:

.. code-block:: python

    import datajoint as dj
    schema = dj.schema('alice_experiment', locals())

This statement creates the database ``alice_experiment`` on the server.  
The second argument of ``dj.schema`` is the contexts in which future table declarations will look for other classes; this argument will nearly always need to be simply ``locals()``.

The returned object ``schema`` will then serve as a decorator for DataJoint classes, as described in :doc:`Create-tables`.

It is a common practice to have a separate Python module for each schema.  Therefore, each such module has only one ``dj.schema`` object defined and is usually named ``schema``.

Working with existing data
--------------------------
What if the database already exists?  For example, what if we created the schema in Python but want to access the data from MATLAB or vice versa?  No problem.  Follow the same process for creating the schema and specify the existing database name.  We will show how to work with existing tables later.

.. |matlab| image:: ../_static/img/matlab-tiny.png
.. |python| image:: ../_static/img/python-tiny.png
