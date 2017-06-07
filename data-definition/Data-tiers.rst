Data Tiers
==========

DataJoint assigns all tables to one of the following data tiers that
differentiate how the data originate.

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
     - Small tables containing general facts and settings of 
       the data pipeline; not specific to any experiment or dataset.
   * - **Manual**
     - ``dj.Manual``
     - 
     - Data entered from outside the pipeline
   * - **Imported**
     - ``dj.Imported``
     - ``_``
     - Data computed automatically inside the pipeline but requires
       access to data outside the pipeline.
   * - **Computed**
     - ``dj.Computed``
     - ``__``
     - Data computed automatically entirely inside the pipeline.

Table tiers indicate to database administrators how valuable the data
are. For example, manual data are most valuable. Computed data can
always be deleted and recomputed. Therefore, database administrators may
opt not to back up computed data, for example, or to back up imported
data less frequently than manual data.

The internal prefix is used for for table names on the server side as
described below. These are never visible to the user but database admins
can use these prefixes to set different backup and access policies.

Furthermore, the classes for *imported* and *computed* tables have
additional capabilities for automated processing as described in
:doc:`../computation/Auto-populate`.

Specifying a table's tier
~~~~~~~~~~~~~~~~~~~~~~~~~

The tier of a table is specified by the superclass of its class.

Part tables
~~~~~~~~~~~

:doc:`../computation/Part-tables` do not have their own tier. Instead,
they share the same tier as their master table.

Internal conventions for naming tables
--------------------------------------

On the server side, DataJoint uses the following naming scheme to
generate the table name corresponding to a given class:

First, the name of the class is converted from ``CamelCase`` to
``underscore_delimited_words``. Then the name is prefixed according to
the :doc:`Data-tiers`.

For example:

The table for the class ``StructuralScan`` subclassing ``dj.Manual``
will be named ``structural_scan``.

The table for the class ``SpatialFilter`` subclassing ``dj.Lookup`` will
be named ``#spatial_filter``.

:doc:`../computation/Part-tables` are treated differently. They are
prefixed by the name of their master table, separated by two
underscores.

For example, the table for the class ``Channel(dj.Part)`` with the
master ``Ephys(dj.Imported)`` will be named ``_ephys__channel``.

DataJoint users do not need to know these conventions. However, database
administrators may set backup policies and use access based on data
tiers using these patters.
