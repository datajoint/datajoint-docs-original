.. progress 2 100% Dimitri

.. _transactions:

Transactions
============

In some cases, a sequence of several operations must be performed as a single operation: 
interrupting the sequence of such operations halfway would leave the data in an invalid state. 
While the sequence is in progress, other processes accessing the database will not see the partial results until the transaction is complete.
The sequence make include :ref:`data queries <queries>` and :ref:`manipulations <data-manipulation>`. 

In such cases, the sequence of operations may be enclosed in a **transaction**. 

.. include:: 3-Transactions_lang1.rst
