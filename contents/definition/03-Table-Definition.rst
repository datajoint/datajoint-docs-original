.. progress: 16 30% Austin

.. _definitions:

Table Definition
================

DataJoint models data as sets of **entities** with shared **attributes**, often visualized as tables with rows and columns.
Each row represents a single entity and the values of all of its attributes.
Each column represents a single attribute with a name and a datatype, applicable to entity in the table.
Unlike rows in a spreadsheet, entities in DataJoint don't have names or numbers: they can only be identified by the values of their attributes.
Defining a table means defining the names and datatypes of the attributes as well as the constraints to be applied to those attributes.
Both MATLAB and Python use the same syntax define tables.

For example, the following code in defines the table ``User``, that contains users of the database:


.. include:: 03-Table-Definition_lang1.rst

This defines the class ``User`` that creates the table in the database and provides all its data manipulation functionality.

Table creation on the database server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Users do not need to do anything special to have the table created in the database.
If it is not already defined, it will get automatically created as soon as it is necessary.

.. include:: 03-Table-Definition_lang2.rst


Changing the definition of an existing table
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once the table is created in the database, the definition string has no further effect.
In other words, changing the definition string in the class of an existing table will not actually update the table definition.
To change the table definition, one must first :ref:`drop <drop>` the existing table.
This means that all the data will be lost, and the new definition will be applied to create the new empty table.

Therefore, in the initial phases of designing a DataJoint pipeline, it is common to experiment with variations of the design before populating it with substantial amounts of data.

It is possible to modify a table without dropping it.
This topic is covered separately.

Reverse-engineering the table definition
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

DataJoint objects provide the ``describe`` method, which displays the table definition used to define the table when it was created in the database.
This definition may differ from the definition string of the class if the definition string has been edited after creation of the table.

Examples
--------



.. include:: 03-Table-Definition_lang3.rst


.. include:: 03-Table-Definition_lang4.rst

.. |matlab| image:: ../_static/img/matlab-tiny.png
.. |python| image:: ../_static/img/python-tiny.png
