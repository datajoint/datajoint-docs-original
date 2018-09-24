.. progress: 3.0 30% Dimitri

Drop
====

The ``drop`` method completely removes a table from the database, including its definition.
It also removes all dependent tables, recursively.
DataJoint will first display the tables being dropped and the number of entities in each before prompting the user for confirmation to proceed.

The ``drop`` method is often used during initial design to allow altered table definitions to take effect.

.. matlab 1 start

|matlab| MATLAB
---------------

.. code-block:: matlab

    % drop the Person table from the lab schema
    drop(lab.Person)

.. matlab 1 end

.. python 1 start

|python| Python
---------------

.. code-block:: python

    # drop the Person table from its schema
    Person.drop()

.. python 1 end

.. |python| image:: ../_static/img/python-tiny.png
.. |matlab| image:: ../_static/img/matlab-tiny.png


.. python 2 start

Dropping part tables
--------------------

A :doc:`part tables <../computation/04-master-part>` is usually removed as a consequence of calling ``drop`` on its master table.
To enforce this workflow, calling ``drop`` directly on a part table produces an error.
In some cases, it may be necessary to override this behavior.
To remove a part table without removing its master, use the argument ``force=True``.

.. python 2 end
