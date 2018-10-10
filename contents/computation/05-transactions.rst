.. progress: 3.0 50% Dimitri

.. _make-transactions:

Transactions in Make
=====================

Each call of the :ref:`make` method is enclosed in a transaction.
DataJoint users do not need to explicitly manage transactions but must be aware of their use.

Transactions produce two effects:

First, the state of the database appears stable within the ``make`` call  throughout the transaction:
two executions of the same query  will yield identical results within the same ``make`` call.

Second, any changes to the database (inserts) produced by the ``make`` method will not become visible to other processes until the ``make`` call completes execution.
If the ``make`` method raises an exception, all changes made so far will be discarded and will never become visible to other processes.

Transactions are particularly important to maintain :ref:`group-integrity` using :ref:`master-part`.
The ``make`` call of a master table first inserts the master entity and then inserts all the matching part entities in the part tables.
None of the entities become visible to other processes until the entire ``make`` call completes, at which point they all become visible.
