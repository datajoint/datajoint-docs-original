.. progress: 12.0 30% Austin

.. _table:

Creating Tables
===============

Classes represent tables
------------------------

To make it easy to work with tables in MATLAB and Python, DataJoint programs create a separate class for each table.
Computer programmers refer to this concept as `object-relational mapping <https://en.wikipedia.org/wiki/Object-relational_mapping>`_.
For example, the class ``experiment.Subject`` in MATLAB or Python may correspond to the table called ``subject`` on the database server.
Users never need to see the database directly; they only interact with data in the database by creating and interacting with DataJoint classes.

Data tiers
^^^^^^^^^^
The table class must inherit from one of the following superclasses to indicate its data tier: ``dj.Lookup``, ``dj.Manual``, ``dj.Imported``, ``dj.Computed``, or ``dj.Part``.
See :ref:`tiers` and :doc:`../computation/04-master-part`.

Defining a table
----------------

.. matlab 1 start

|matlab| MATLAB
^^^^^^^^^^^^^^^

DataJoint for MATLAB provides the interactive script ``dj.new`` for creating a new table.
It will prompt to enter the new table's class name in the form ``package.ClassName``.
This will create the file ``+package/ClassName.m``.

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

While ``dj.new`` adds a little bit of convenience, some users may create the classes from scratch manually.

Each newly created class must inherit from the DataJoint class corresponding to the correct :ref:`data tier <tier>`: ``dj.Lookup``, ``dj.Manual``, ``dj.Imported`` or ``dj.Computed``.

The most important part of the table definition is the comment preceding the ``classdef``.
DataJoint will parse this comment to define the table.

The class will become usable after you edit this comment as described in :ref:`definitions`.
.. matlab 1 end

.. python 1 start

|python| Python
^^^^^^^^^^^^^^^^^^^^^^^^^^^

To define a DataJoint table in Python:

1. Define a class inheriting from the appropriate DataJoint class: ``dj.Lookup``, ``dj.Manual``, ``dj.Imported`` or ``dj.Computed``.

2. Decorate the class with the schema object (See :ref:`schema`)

3. Define the class property ``definition`` to define the table heading.

For example, the following code defines the table ``Person``:

.. code-block:: python

	import datajoint as dj
	schema = dj.schema('alice_experiment')

	@schema
	class Person(dj.Manual):
	    definition = '''
	    # table definition goes here
	    '''


The ``@schema`` decorator uses the class name and the data tier to check whether an appropriate table exists on the database.
If a table does not already exist, the decorator creates one on the database using the definition property.
The decorator attaches the information about the table to the class, and then returns the class.

The class will become usable after you define the ``definition`` property as described in :ref:`definitions`.

DataJoint classes in Python
~~~~~~~~~~~~~~~~~~~~~~~~~~~

DataJoint for Python is implemented through the use of classes.
Working with classes usually implies that one might create different class instances with various internal states.
However, DataJoint classes only serve as interfaces to data that actually reside within tables on the database server.
Whether calling a DataJoint method on a class or on an instance, the result will only depend on or apply to the corresponding table.
All of the basic functionality of DataJoint is built to operate on the classes themselves, even when called on an instance.
For example, calling ``Person.insert(...)`` (on the class) and ``Person.insert(...)`` (on an instance) both have the identical effect of inserting data into the table on the database server.
DataJoint does not prevent a user from working with instances, but the workflow is complete without the need for instantiation.
It is up to the user whether to implement additional functionality as class methods or methods called on instances.
.. python 1 end

Valid class names
------------------
Note that in both MATLAB and Python, the class names must follow the CamelCase compound word notation:

* start with a capital letter and
* contain only alphanumerical characters (no underscores).

Examples of valid class names:

``TwoPhotonScan``, ``Scan2P``, ``Ephys``, ``MembraneVoltage``

Invalid class names:

``Two_photon_Scan``, ``twoPhotonScan``, ``2PhotonScan``, ``membranePotential``, ``membrane_potential``


.. |python| image:: ../_static/img/python-tiny.png
.. |matlab| image:: ../_static/img/matlab-tiny.png
