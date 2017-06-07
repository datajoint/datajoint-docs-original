Table Definition
================

Defining a table means to define the columns of the table (their names and datatypes) and constraints to be applied to them.

Both MATLAB and Python use the same syntax define tables.  In Python, the table definition is contained in the ``definition`` property of the class.  In MATLAB, the table definition is contained in the first block comment in the class definition file.  Note that although it looks like a mere comment, the table definition in MATLAB is parsed by DataJoint.  This solution thought to be convenient since MATLAB does not provide convenient syntax for multiline strings. 

Tables have rows and columns.  Each column has a name and a datatype.  Rows don't have names or numbers and can only be identified by their contents.

For example, the following code in MATLAB and Python defines the same table, ``User`` that contains users of the database:

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
Users do not need to do anything special to have the table created in the database.  If it is not already defined, it will get automatically created as soon as it is necessary.  

In Python, the table is created at the time of the class definition.  In fact, it is one of the jobs performed by the decorator ``@schema`` of the class.

In MATLAB, the table is created up the first attempt to use the class for manipulating its data (e.g. inserting tuples or fetching tuples).


Changing the definition of an existing table
--------------------------------------------
Once the table is created in the database, the definition string has no effect.  To change the table definition, one must [drop the table](Drop) first.  This means all the data will be lost and the new definition will applied to create the new empty table. 

Therefore, in the initial phases of designing a DataJoint pipeline, it is common to experiment with various variations of the design before populating it with substantial amounts of data.

It is possible to modify a table without dropping it.  This topic is covered separately.

Reverse-engineering the table definition
----------------------------------------

DataJoint objects provide the ``describe`` method to see the table definition to define the table that is actually in the database.  This definition may differ from the one in the definition string if the definition string has been edited or if the definition has been changed by someone else. 

Examples
++++++++
|matlab| MATLAB

.. code-block:: matlab

	s = describe(lab.User)
	
|python| Python

.. code-block:: python

	s = lab.User().describe()

Furthermore, DataJoint for MATLAB provides the ``syncDef`` method to update the ``classdef`` file for the relation with the actual table definition:


|matlab| MATLAB

.. code-block:: matlab

	syncDef(lab.User)    % updates the table definition in file +lab/User.m

Python does not provide such a method because classes in Python are not always linked to an editable file.

.. |matlab| image:: ../_static/img/matlab-tiny.png
.. |python| image:: ../_static/img/python-tiny.png

