.. progress: 6.0 10% Dimitri

Delete
======

The ``delete`` (Python) and ``del`` (MATLAB) method deletes entities from a table and all dependent entries in dependent tables.
Delete is often used in conjunction with the :doc:`../queries/05-Restriction` operator to define the subset of entities to delete.
Delete is performed as an atomic transaction so that partial deletes never occur.

.. matlab 1 start

|matlab| MATLAB examples
------------------------
Delete the entire contents of the table ``tuning.VonMises`` and all its dependents:

.. code-block:: matlab

    % delete all entries from tuning.VonMises
    del(tuning.VonMises)

    % delete entries from tuning.VonMises for mouse 1010
    del(tuning.VonMises & 'mouse=1010')

    % delete entries from tuning.VonMises except mouse 1010
    del(tuning.VonMises - 'mouse=1010')
.. matlab 1 end

.. python 1 start

|python| Python examples
------------------------

.. code-block:: python

    # delete all entries from tuning.VonMises
    tuning.VonMises.delete()

    # delete entries from tuning.VonMises for mouse 1010
    (tuning.VonMises & 'mouse=1010').delete()

    # delete entries from tuning.VonMises except mouse 1010
    (tuning.VonMises - 'mouse=1010').delete()
.. python 1 end

.. python 2 start

Deleting from part tables
-------------------------
Entities in a :doc:`part table <../computation/04-master-part>` are usually removed as a consequence of calling ``delete`` on the master table.
To enforce this workflow, calling ``delete`` directly on a part table produces an error.
In some cases, it may be necessary to override this behavior.
To remove entities from a part table without calling ``delete`` master, use the argument ``force=True``.

.. python 2 end

.. |python| image:: ../_static/img/python-tiny.png
.. |matlab| image:: ../_static/img/matlab-tiny.png
