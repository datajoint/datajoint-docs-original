.. progress: 12.0 30% Austin

Creating Tables
===============


Relational data model
---------------------

As already mentioned in :doc:`01-Creating-Schemas`, all data in DataJoint are represented in the form of tables residing in database schemas on the database server.
On the client side, in Python and MATLAB, each table has its own DataJoint class, which defines the table and manipulates its data.

Data tiers
^^^^^^^^^^
The table class must inherit from one of the following superclasses to indicate its data tier: ``dj.Lookup``, ``dj.Manual``, ``dj.Imported``, ``dj.Computed``, or ``dj.Part``.
See :doc:`05-Data-Tiers` and :doc:`../computation/04-master-part`.

Defining a table
----------------

.. include:: 02-Creating-Tables_lang1.rst

-------------------

Valid class names
------------------
Note that in both MATLAB and Python, the class names must follow the CamelCase compound word notation:

* start with a capital letter and
* contain only alphanumerical characters (no underscores).

Examples of valid class names:

``TwoPhotonScan``, ``Scan2P``, ``Ephys``, ``MembraneVoltage``

Invalid class names:

``Two_photon_Scan``, ``twoPhotonScan``, ``2PhotonScan``, ``membranePotential``, ``membrane_potential``


