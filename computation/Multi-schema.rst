
.. TODO:
.. insert_from_select : or is that elsewhere


Working with Schema Objects
===========================

Partitioning data into different datasets can be a useful means to categorize
and manage data according to various criteria, such as data type or longetivty,
data readyness or completeness, data sharing and access, or any number of other
factors. In DataJoint, this kind of data partitioning can be accomplished
through the use of multiple database schemas.

.. TODO: does this hold for Matlab?
This is typically done in one of two main ways:

- Embedding the DataJoint 'schema' object within a language module
  which is then utilized from within another project. This is the most
  typical use case.
- Less frequently, multiple schema objects are created within the same
  language module or processing script with differing names, and
  referenced directly as applicable.
- Sometimes, querying of data tables using DataJoint is desired without
  needing to load the related module code.

Using a Schema via another Module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

|python| Python
---------------

In python, schemas embedded in other modules are used via the table classes
of that schema. For example: 

.. code-block:: python

    import foo
    foo.Foo()

    schema = dj.schema('not_foos_database', locals())

    @schema
    class LocalFooReferrer(dj.Manual):
        definition = """
        myunique:       int     # local unique data
        -> foo.Foo              # foreign key reference to foo's Foo
        """

As can be seen here, other modules can also be used within local table
definitions provided they are properly referenced by the module scope.

Using Multiple Schemas in the same File/Script
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is typically done for data manipulation/processing purposes; Normal use
would usually be via modules as outlined above. 

|python| Python
---------------

In python, using multiple schemas within a single script or session is
done by simply making the schema objects have unique names. For example:

.. code-block:: python

    first_schema = dj.schema('example_first_db', locals())
    second_schema = dj.schema('example_second_db', locals())

    @first_schema
    class FirstTable(dj.Manual):
        definition = """
        firstattr       int     # first attribute
        """

    @second_schema
    class SecondTable(dj.Manual):
        definition = """
        secondattr       int     # second attribute
        """

Using Schemas via Database Introspection
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There are two primary ways to use schemas via Database introspection,
each of which will create basic DataJoint user relations (table
classes) suitable for querying and retrieving associated data within
DataJoint. These are the `spawn_missing_classes` method of a schema
object, which will define the generated classes in the same context
passed into the schema object constructor (typically 'locals()' in
the module where the schema object was first instantiated), and
`dj.create_virtual_module`, which returns a reference to a generated
module containing the generated table classes. A usage example of
each method follows.


|python| Python
---------------

A `spawn_missing_classes` example:

.. code-block:: python

   import datajoint as dj

   # contains Foo(dj.Manual)
   schema = dj.schema('tutorial_foo_db', locals())
   schema.spawn_missing_classes()

   Foo().insert1('foo')

An example of `create_virtual_module`:

.. code-block:: python

   import datajoint as dj

   # contains Foo(dj.Manual)
   v_schema = dj.create_virtual_module('foomod', 'tutorial_foo_db')
   
   v_schema.Foo()

.. |python| image:: ../_static/img/python-tiny.png
.. |matlab| image:: ../_static/img/matlab-tiny.png
