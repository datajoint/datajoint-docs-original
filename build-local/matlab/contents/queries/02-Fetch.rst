.. progress: 6.0  20% Dimitri

.. _fetch:

Fetch
=====

Data queries in DataJoint comprise two distinct steps:

1. Construct the ``query`` object to represent the required data using tables and :ref:`operators`.
2. Fetch the data from ``query`` into the workspace of the host language -- described in this section.

Fetch works somewhat differently between MATLAB and Python.

Note that entities returned by ``fetch`` methods are not guaranteed to be sorted in any particular order unless specifically requested.
Furthermore, the order is not guaranteed to be the same in any two queries, and the contents of two identical queries may change between two sequential invocations unless they are wrapped in a transaction.
Therefore, if you wish to fetch matching pairs of attributes, do so in one ``fetch`` call.

.. include: 02-Fetch_lang1.rst

