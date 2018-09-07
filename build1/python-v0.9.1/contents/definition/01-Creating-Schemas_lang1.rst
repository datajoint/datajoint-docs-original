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

.. |python| image:: ../_static/img/python-tiny.png
