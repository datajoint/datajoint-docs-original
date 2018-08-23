.. progress: 12.0 30% Austin

Create Tables
=============


Relational Data Model
---------------------

As already mentioned in :doc:`01-create-schema`, all data in DataJoint are represented in the form of tables residing in databases on the database server.  On the client side, in Python and MATLAB, each table has its own DataJoint class, which defines the table and manipulates its data.

Data Tiers
^^^^^^^^^^
The table class must inherit from one of the following superclasses: ``dj.Lookup``, ``dj.Manual``, ``dj.Imported``, ``dj.Computed``, or ``dj.Part`` to indicate its data tier.  See :doc:`05-tiers` and :doc:`../computation/04-master-part`.

Defining a table
----------------


|matlab| MATLAB
^^^^^^^^^^^^^^^


DataJoint for MATLAB provides the interactive script ``dj.new`` for creating a new table.  It will prompt to enter the new table's class name in the form ``package.ClassName``.  This will create the file ``+package/ClassName.m``.

For example, define the table ``experiment.Person``

.. code-block:: matlab

	>> dj.new
	Enter <package>.<ClassName>: experiment.Person

	Choose table tier:
	  L=lookup
	  M=manual
	  I=imported
	  C=computed
	  P=part
	 (L/M/I/C/P) > M

This will create the file ``+experiment/Person.m`` with the following contents:

.. code-block:: matlab 

	%{
	# my newest table
	# add primary key here
	-----
	# add additional attributes
	%}

	classdef Person < dj.Manual
	end

``dj.new`` adds a little bit of convenience while some users may create the classes from scratch manually.

The important part is that the class inherits from the DataJoint class corresponding to the correct [data tier](Data tiers): ``dj.Lookup``, ``dj.Manual``, ``dj.Imported`` or ``dj.Computed``. 

The most important part of the table definition is the comment preceding the ``classdef``.  DataJoint will parse this comment to define the table.

The class will become usable after you edit this comment as described in :doc:`03-table-definition`.

|python| Python
^^^^^^^^^^^^^^^^^^^^^^^^^^^

To define a DataJoint table in Python:
1. Define a class inheriting from the appropriate DataJoint class: ``dj.Lookup``, ``dj.Manual``, ``dj.Imported`` or ``dj.Computed``.
2. Decorate the class with the schema object (See :doc:`01-create-schema`)
3. Define the class property ``definition`` to define the table heading.

For example, the following code defines the table ``Person``:

.. code-block:: python

	import datajoint as dj
	schema = dj.schema('alice_experiment', locals())

	@schema 
	class Person(dj.Manual):
	    definition = '''
	    # table definition goes here
	    '''


The class will become usable after you edit the ``definition`` property as described in :doc:`03-table-definition`.

-------------------

Valid class names
=================
Note that in both MATLAB and Python, the class names must follow the CamelCase compound word notation: 
* start with a capital letter and 
* contain only alphanumerical characters (no underscores).  

Examples: 
 
Valid class names:

``TwoPhotonScan``, ``Scan2P``, ``Ephys``, ``MembraneVoltage`` 

Invalid class names:

``Two_photon_Scan``, ``twoPhotonScan``, ``2PhotonScan``, ``membranePotential``, ``membrane_potential``


.. |python| image:: ../_static/img/python-tiny.png
.. |matlab| image:: ../_static/img/matlab-tiny.png
