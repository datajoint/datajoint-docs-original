|python| Python
^^^^^^^^^^^^^^^^^^^^^^^^^^^

To define a DataJoint table in Python:

1. Define a class inheriting from the appropriate DataJoint class: ``dj.Lookup``, ``dj.Manual``, ``dj.Imported`` or ``dj.Computed``.

2. Decorate the class with the schema object (See :doc:`01-Creating-Schemas`)

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


The class will become usable after you edit the ``definition`` property as described in :doc:`03-Table-Definition`.


.. |python| image:: ../_static/img/python-tiny.png
