Table Definition
=================

.. toctree::
   :maxdepth: 6
   :hidden:
   :titlesonly:
   :includehidden:

   Data-types
   Primary-key
   Foreign-keys

Defining a table means to define the columns of the table (their names and datatypes) and constraints to be applied to them.

Both MATLAB and Python use the same syntax define tables.  In Python, the table definition is contained in the ``definition`` property of the class.  In MATLAB, the table definition is contained in the first block comment in the class definition file.  Note that although it looks like a mere comment, the table definition in MATLAB is parsed by DataJoint.  This solution thought to be convenient since MATLAB does not provide convenient syntax for multiline strings. 

Tables have rows and columns.  Each column has a name and a datatype.  Rows don't have names or numbers and can only be identified by their contents.

For example, the following code in MATLAB and Python defines the same table, ``User`` that contains users of the database:

MATLAB:

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


Python:

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

Attribute names
^^^^^^^^^^^^^^^^^^^^
Attribute names must be in lowercase and must start with a letter.  They can only contain alphanumerical characters and underscores.  The attribute name cannot exceed 64 characters.

Valid attribute names
+++++++++++++++++++++++++++
``first_name``, ``two_photon_scan``, ``scan_2p``, ``two_photon_scan_``

Invalid attribute names
++++++++++++++++++++++++++++
``firstName``, ``first name``, ``2photon_scan``, ``two-photon_scan``, ``TwoPhotonScan``

Table definition format
^^^^^^^^^^^^^^^^^^^^^^^^^
The table definition consist of lines.  Each line can be one of the following:
* The optional first line starting with a ``#`` provides a description of the table's purpose. It may also be thought of as the table's long title.
* A new attribute definition in the format ``name = default : datatype  # comment``, where the default and the comment are optional. (See :doc:`Data-types`.)
* The divider ``---`` (at least three dashes) separating primary key attributes above from non-primary attributes below.
* A foreign key in the format ``-> ReferencedTable``. (See :doc:`Foreign-keys`.)

For example, the table for Persons may have the following definition:

.. code-block:: python

	# Persons in the lab
	username :  varchar(16)   #  username in the database
	---
	full_name : varchar(255)   
	start_date :  date   # date when joined the lab


This will define the table with columns ``username``, ``full_name``, and ``start_date``, in which ``username`` is the :doc:`Primary-key`.

When do tables get created?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Users do not need to do anything special to have the table created in the database.  If it is not already defined, it will get automatically created as soon as it is necessary.  

In Python, the table is created at the time of the class definition.  In fact, it is one of the jobs performed by the decorator ``@schema`` of the class.

In MATLAB, the table is created up the first attempt to use the class for manipulating its data (e.g. inserting tuples or fetching tuples).

Changing the definition of an existing table
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Once the table is created in the database, the definition string has no effect.  To change the table definition, one must [drop the table](Drop) first.  This means all the data will be lost and the new definition will applied to create the new empty table. 

Therefore, in the initial phases of designing a DataJoint pipeline, it is common to experiment with various variations of the design before populating it with substantial amounts of data.

It is possible to modify a table without dropping it.  This topic is covered separately in [[Modifying designs]].

Reverse-engineering the table definition
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
DataJoint objects provide the ``describe`` method to see the table definition to define the table that is actually in the database.  This definition may differ from the one in the definition string if the definition string has been edited or if the definition has been changed by someone else. 

Examples
+++++++++++++
MATLAB

.. code-block:: matlab

	s = describe(lab.User)
	
Python

.. code-block:: python

	s = lab.User().describe()

Furthermore, DataJoint for MATLAB provides the ``syncDef`` method to update the ``classdef`` file for the relation with the actual table definition:

.. code-block:: matlab

	syncDef(lab.User)    % updates the table definition in file +lab/User.m

Python does not provide such a method because classes in Python are not always linked to an editable file.


