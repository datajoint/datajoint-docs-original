.. progress: 16 30% Austin

Table Definition
================

Defining a table means defining the columns of the table (their names and datatypes) and the constraints to be applied to those collumns.

Both MATLAB and Python use the same syntax define tables.
In Python, the table definition is contained in the ``definition`` property of the class.
In MATLAB, the table definition is contained in the first block comment in the class definition file.
Note that although it looks like a mere comment, the table definition in MATLAB is parsed by DataJoint.
This solution is thought to be convenient since MATLAB does not provide convenient syntax for multiline strings.

Tables have rows and columns.
Each column has a name and a datatype.
We refer to columns in DataJoint as *attributes*.

Rows in Datajoint don't have names or numbers; they can only be identified by their contents.
We often refer to rows as *entities* in DataJoint.

For example, the following code in MATLAB and Python defines the same table, ``User``, that contains users of the database:

|matlab| MATLAB

.. code-block:: matlab

	%{
	# database users
	username : varchar(20)   # unique user name
	---
	first_name : varchar(30)
	last_name  : varchar(30)
	role : enum('admin', 'contributor', 'viewer')
	%}
	classdef User < dj.Manual
	end


|python| Python

.. code-block:: python

	@schema
	class User(dj.Manual):
	    definition = """
	    # database users
	    username : varchar(20)   # unique user name
	    ---
	    first_name : varchar(30)
	    last_name  : varchar(30)
	    role : enum('admin', 'contributor', 'viewer')
	    """


Both define the class `User` that creates the table in the database and provides all its data manipulation functionality.


When are the tables created?
----------------------------
Users do not need to do anything special to have the table created in the database.
If it is not already defined, it will get automatically created as soon as it is necessary.

In Python, the table is created at the time of the class definition.
In fact, it is one of the jobs performed by the decorator ``@schema`` of the class.

In MATLAB, the table is created upon the first attempt to use the class for manipulating its data (e.g. inserting or fetching entities).


Changing the definition of an existing table
--------------------------------------------
Once the table is created in the database, the definition string has no further effect.
In other words, changing the definition string in the class of an existing table will not actually update the table definition.
To change the table definition, one must :doc:`drop the table <13-Drop>` first.
This means that all the data will be lost, and the new definition will be applied to create the new empty table.

Therefore, in the initial phases of designing a DataJoint pipeline, it is common to experiment with variations of the design before populating it with substantial amounts of data.

It is possible to modify a table without dropping it.
This topic is covered separately.

Reverse-engineering the table definition
----------------------------------------

DataJoint objects provide the ``describe`` method, which displays the table definition used to define the table when it was created in the database.
This definition may differ from the definition string of the class if the definition string has been edited after creation of the table.

Examples
++++++++
|matlab| MATLAB

.. code-block:: matlab

	s = describe(lab.User)

|python| Python

.. code-block:: python

	s = lab.User().describe()

Furthermore, DataJoint for MATLAB provides the ``syncDef`` method to update the ``classdef`` file definition string for the table with the definition in the actual table:


|matlab| MATLAB

.. code-block:: matlab

	syncDef(lab.User)    % updates the table definition in file +lab/User.m

Python does not provide such a method because classes in Python are not always linked to an editable file.

.. |matlab| image:: ../_static/img/matlab-tiny.png
.. |python| image:: ../_static/img/python-tiny.png
