.. progress: 3.0 50% Dimitri

.. _tiers:

Data Tiers
==========

DataJoint assigns all tables to one of the following data tiers that differentiate how the data originate.

.. list-table:: Table tiers
   :widths: 15 20 20 30
   :header-rows: 1

   * - Tier
     - Superclass
     - Prefix
     - Description
   * - **Lookup**
     - ``dj.Lookup``
     - ``#``
     - Small tables containing general facts and settings of the data pipeline; not specific to any experiment or dataset.
   * - **Manual**
     - ``dj.Manual``
     -
     - Data entered from outside the pipeline, either by hand or with external helper scripts.
   * - **Imported**
     - ``dj.Imported``
     - ``_``
     - Data ingested automatically inside the pipeline but requiring access to data outside the pipeline.
   * - **Computed**
     - ``dj.Computed``
     - ``__``
     - Data computed automatically entirely inside the pipeline.

Table data tiers indicate to database administrators how valuable the data are.
Manual data are the most valuable, as re-entry may be tedious or impossible.
Computed data are safe to delete, as the data can always be recomputed from within DataJoint.
Imported data are safer than manual data but less safe than computed data because of dependency on external data sources.
With these considerations, database administrators may opt not to back up computed data, for example, or to back up imported data less frequently than manual data.

The internal prefixes listed above are used for table names on the server side as described below.
These are never visible to the user, but database admins can use these prefixes to set different backup and access policies.

Furthermore, the classes for **imported** and **computed** tables have additional capabilities for automated processing as described in :ref:`auto`.

Specifying a table's tier
-------------------------

The data tier of a table is specified by the superclass of its class.
For example, the User class in :ref:`definitions` uses the ``dj.Manual`` superclass.
Therefore, the corresponding User table on the database would be of the Manual tier.

Internal conventions for naming tables
--------------------------------------

On the server side, DataJoint uses the following naming scheme to generate the table name corresponding to a given class:

First, the name of the class is converted from ``CamelCase`` to ``snake_case`` (`separation by underscores <https://en.wikipedia.org/wiki/Snake_case>`_).
Then the name is prefixed according to the data tier.

For example:

The table for the class ``StructuralScan`` subclassing ``dj.Manual`` will be named ``structural_scan``.

The table for the class ``SpatialFilter`` subclassing ``dj.Lookup`` will be named ``#spatial_filter``.

Again, DataJoint users do not need to know these conventions, but database administrators may use these naming patterns to set backup policies or to restrict access based on data tiers.

Part tables
-----------

:ref:`Part tables <part>` do not have their own tier.
Instead, they share the same tier as their master table.
The prefix for part tables also differs from the other tiers.
They are prefixed by the name of their master table, separated by two underscores.

For example, the table for the class ``Channel(dj.Part)`` with the master ``Ephys(dj.Imported)`` will be named ``_ephys__channel``.
