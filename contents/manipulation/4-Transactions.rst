.. progress 2 100% Dimitri

.. _transactions:

Transactions
============

In some cases, a sequence of several operations must be performed as a single operation: 
interrupting the sequence of such operations half-way would leave the data in an invalid state. 
While the sequence is progress, other users of the database must not see the partial results. 
The sequence make include :ref:`data queries <queries>` and :ref:`manipulations <data-manipulation>`. 

In such cases, the sequence of operations may be enclosed in a *transaction*. 

.. include:: 3-Transactions_lang1.rst

