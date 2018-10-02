.. progress: 3.0 30% Dimitri

.. _drop:

Drop
====

The ``drop`` method completely removes a table from the database, including its definition.
It also removes all dependent tables, recursively.
DataJoint will first display the tables being dropped and the number of entities in each before prompting the user for confirmation to proceed.

The ``drop`` method is often used during initial design to allow altered table definitions to take effect.

.. include:: 14-Drop_lang1.rst


.. |python| image:: ../_static/img/python-tiny.png
.. |matlab| image:: ../_static/img/matlab-tiny.png



.. include:: 14-Drop_lang2.rst
