.. progress: 6.0 10% Dimitri

Delete
======

The ``delete`` (Python) and ``del`` (Matlab) method deletes tuples from a table and all dependent entries in dependent tables.
Delete is often used in conjunction with the :doc:`../queries/04-restriction` operator to define the subset of tuples to delete.  Delete is performed as an atomic transaction so that partial deletes never occur.

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

|python| Python examples
------------------------

.. code-block:: python

    # delete all entries from tuning.VonMises
    tuning.VonMises.delete()

    # delete entries from tuning.VonMises for mouse 1010
    (tuning.VonMises & 'mouse=1010').delete()

    # delete entries from tuning.VonMises except mouse 1010
    (tuning.VonMises - 'mouse=1010').delete()


Deleting from part tables
-------------------------
:doc:`../computation/04-master-part` prohibit direct deletion. The only way to delete from a part table is to delete from its master.

.. |python| image:: ../_static/img/python-tiny.png
.. |matlab| image:: ../_static/img/matlab-tiny.png
