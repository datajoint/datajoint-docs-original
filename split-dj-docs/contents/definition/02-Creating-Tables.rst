.. progress: 12.0 30% Austin

.. _table:

Creating Tables
===============

Classes represent tables
------------------------

To make it easy to work with tables in MATLAB and Python, DataJoint programs create a separate class for each table.
Computer programmers refer to this concept as `object-relational mapping <https://en.wikipedia.org/wiki/Object-relational_mapping>`_.
For example, the class ``experiment.Subject`` in MATLAB or Python may correspond to the table called ``subject`` on the database server.
Users never need to see the database directly; they only interact with data in the database by creating and interacting with DataJoint classes.

Data tiers
^^^^^^^^^^
The table class must inherit from one of the following superclasses to indicate its data tier: ``dj.Lookup``, ``dj.Manual``, ``dj.Imported``, ``dj.Computed``, or ``dj.Part``.
See :ref:`tiers` and :ref:`master-part`.

Defining a table
----------------


.. include:: 02-Creating-Tables_lang1.rst

Valid class names
------------------
Note that in both MATLAB and Python, the class names must follow the CamelCase compound word notation:

* start with a capital letter and
* contain only alphanumerical characters (no underscores).

Examples of valid class names:

``TwoPhotonScan``, ``Scan2P``, ``Ephys``, ``MembraneVoltage``

Invalid class names:

``Two_photon_Scan``, ``twoPhotonScan``, ``2PhotonScan``, ``membranePotential``, ``membrane_potential``


.. |python| image:: ../_static/img/python-tiny.png
.. |matlab| image:: ../_static/img/matlab-tiny.png
