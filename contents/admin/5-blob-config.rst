.. progress: 16.0 50% Dimitri

.. _external:

External Store
==============

DataJoint organizes most of its data in a relational database.
Relational databases excel at representing relationships between entities and storing structured data.
However, relational databases are not particularly well-suited for storing large continuous chunks of data such as images, signals, and movies.
An attribute of type ``longblob`` can contain an object up to 4 GiB in size (after compression) but storing many such large objects may hamper the performance of queries on the entire table.
A good rule of thumb is that objects over 10 MiB in size should not be put in the relational database.
In addition, storing data in cloud-hosted relational databases (e.g. AWS RDS) may be more expensive than in cloud-hosted simple storage systems (e.g. AWS S3).

DataJoint allows the use of `external` storage to store large data objects within its relational framework but outside of the main database.

Defining an externally-stored attribute is used using the notation ``blob@storename`` (see also: :ref:`definition syntax <definitions>`) and works the same way as a ``longblob`` attribute from the users perspective. However, its data are stored in an external storage system rather than in the relational database.

Various systems can play the role of external storage, including a shared file system accessible to all team members with access to these objects or a cloud storage solutions such as AWS S3.

For example, the following table stores motion-aligned two-photon movies.

.. code-block:: text

    # Motion aligned movies
    -> twophoton.Scan
    ---
    aligned_movie :  blob@external  # motion-aligned movie in 'external' store


All :ref:`insert <insert>` and :ref:`fetch <fetch>` operations work identically for ``external`` attributes as they do for blob attributes, with the same serialization protocol.
Similar to blobs, external attributes cannot be used in restriction conditions.

Multiple external storage configurations may be used simultaneously with the ``@storename`` portion of the attribute definition determining the storage location.

.. code-block:: text

    # Motion aligned movies
    -> twophoton.Scan
    ---
    aligned_movie :  blob@external-raw  # motion-aligned movie in 'external-raw' store

Principles of operation
-----------------------
External storage is organized to emulate individual attribute values in the relational database.
DataJoint organizes external storage to preserve the same data integrity principles as in relational storage.

1. The external storage locations are specified in the DataJoint connection configuration, with one specification for each store.

.. include:: 5-blob-config_lang1.rst

2. Each schema corresponds to a dedicated folder at the storage location with the same name as the database schema.

3. Stored objects are identified by the `SHA-256 <https://en.wikipedia.org/wiki/SHA-2>`_ hashes (in web-safe base-64 ASCII) of their serialized contents.
   This scheme allows for the same object used multiple times in the same schema to be stored only once.

4. In the external storage, the objects are saved as files with the hash as the filename. 

5. In the external storage, external files are stored in a directory layout corresponding to the hash of the filename. By default, this corresponds to the first 2 characters of the hash, followed by the second 2 characters of the hash, followed by the actual file.

6. Each database schema has an auxiliary table named ``~external_<storename>`` for each configured external store.

   It is automatically created the first time external storage is used.
   The primary key of ``~external_<storename>`` is the hash of the data (for blobs and attachments) or of the relative paths to the files for filepath-based storage.
   Other attributes are the ``count`` of references by tables in the schema, the ``size`` of the object in bytes, and the timestamp of the last event (creation, update, or deletion).

   Below are sample entries in ``~external_<storename>``.

   .. only:: latex

      .. list-table:: ~external_raw
            :widths: 3 10 2 3 5
            :header-rows: 1

            * - HASH
              - size
              - filepath
              - contents_hash
              - timestamp
            * - 1GEqtEU6JYEOLS4sZHeHDxWQ3JJfLlH VZio1ga25vd2
              - 1039536788
              - NULL
              - NULL
              - 2017-06-07 23:14:01

   .. only:: html

        .. |br| unicode::  U+2028 .. line separator
            :trim:

        .. list-table:: ~external_raw
            :widths: auto
            :header-rows: 1
            :align: center

            * - HASH
              - size
              - filepath
              - contents_hash
              - timestamp
            * - 1GEqtEU6JYE |br| OLS4sZHeHDx |br| WQ3JJfLlHVZ |br| io1ga25vd2
              - 1039536788
              - NULL
              - NULL
              - 2017-06-07 23:14:01

   The fields `filepath` and `contents_hash` relate to the `filepath` datatype, which will be discussed separately.

7. Attributes of type ``@<storename>`` are declared as renamed :ref:`foreign keys <dependencies>` referencing the ``~external_<storename>`` table (but are not shown as such to the user).

8. The :ref:`insert <insert>` operation encodes and hashes the blob data. If an external object is not present in storage for the same hash, the object is saved and if the save operation is successful, a corresponding entities in ``~external_<storename>`` table for that store is created.

9. The :ref:`delete <delete>`  operation first deletes the foreign key reference in the target table. The external table entry and actual external object is not actually deleted at this time (`soft-delete`).

10. The :ref:`fetch <fetch>` operation uses the hash values to find the data.
   In order to prevent excessive network overhead, a special external store named ``cache`` can be configured.
   If the ``cache`` is enabled, the ``fetch`` operation need not access ``~external_<storename>`` directly.
   Instead ``fetch`` will retrieve the cached object without downloading directly from the `real` external store.

11. Cleanup is performed regularly when the database is in light use or off-line.

12. DataJoint never removes objects from the local ``cache`` folder.
    The ``cache`` folder may just be periodically emptied entirely or based on file access date.
    If dedicated ``cache`` folders are maintained for each schema, then a special procedure will be provided to remove all objects that are no longer listed in ``~external_<storename>``.

Data removal from external storage is separated from the delete operations to ensure that data are not lost in race conditions between inserts and deletes of the same objects, especially in cases of transactional processing or in processes that are likely to get terminated.
The cleanup steps are performed in a separate process when the risks of race conditions are minimal.
The process performing the cleanups must be isolated to prevent interruptions resulting in loss of data integrity.

Configuration
-------------
The following steps must be performed to enable external storage:

1. Assign external location settings for each storage as shown in the Step 1 example above.

  .. include:: 5-blob-config_lang2.rst

  ``location`` specifies the root path to the external data for all schemas as well as the protocol in the prefix such as ``file://`` or ``s3://``.

  ``account`` and ``token`` specify the credentials for accessing the external location.

2. Optionally, for each schema specify the cache folder for local fetch cache.

.. include:: 5-blob-config_lang3.rst

Cleanup
-------

Deletion of records containing externally stored blobs is a `soft-delete` which only removes the database-side records from the database.
To cleanup the external tracking table or the actual external files, a separate process is provided as follows.

.. include:: 5-blob-config_lang4.rst


Migration between DataJoint v0.11 and v0.12
-------------------------------------------

.. note::

  Please read carefully if you have used external storage in DataJoint v0.11!

The initial implementation of external storage was reworked for
DataJoint v0.12. These changes are backward-incompatible with DataJoint
v0.11 so care should be taken when upgrading. This section outlines
some details of the change and a general process for upgrading to a
format compatible with DataJoint v0.12 when a schema rebuild is not
desired.

The primary changes to the external data implementation are:

   - The external object tracking mechanism was modified. Tracking tables
     were extended for additional external datatypes and split into
     per-store tables to improve database performance in schemas with
     many external objects.

   - The external storage format was modified to use a nested subfolder
     structure (`folding`) to improve performance and interoperability
     with some filesystems that have limitations or performance problems
     when storing large numbers of files in single directories.

Depending on the circumstances, the simplest way to migrate data to
v0.12 may be to drop and repopulate the affected schemas. This will construct
the schema and storage structure in the v0.12 format and save the need for
database migration. When recreation is not possible or is not preferred
to upgrade to DataJoint v0.12, the following process should be followed:

  1) Stop write activity to all schemas using external storage.

  2) Perform a full backup of your database(s).

  3) Upgrade your DataJoint installation to v0.12

  4) Adjust your external storage configuration (in `datajoint.config`)
     to the new v0.12 configuration format (see above).

  5) Migrate external tracking tables for each schema to use the new format. For instance in Python:

      >>> import datajoint.migrate as migrate
      >>> db_schema_name='schema_1'
      >>> migrate.migrate_dj011_external_blob_storage_to_dj012(db_schema_name)
    
  6) Verify pipeline functionality after this process has completed::

      >>> x = myschema.TableWithExternal.fetch('external_field', limit=1)[0]

.. note::

  This migration function is provided on a best-effort basis, and will
  convert the external tracking tables into a format which is compatible
  with DataJoint v0.12. While we have attempted to ensure correctness
  of the process, all use-cases have not been heavily tested. Please be sure to fully
  back-up your data and be prepared to investigate problems with the
  migration, should they occur.

Please note:

  - The migration only migrates the tracking table format and does not
    modify the backing file structure to support `folding`. The DataJoint
    v0.12 logic is able to work with this format, but to take advantage
    of the new backend storage, manual adjustment of the tracking table
    and files, or a full rebuild of the schema should be performed.

  - Additional care to ensure all clients are using v0.12 should be
    taken after the upgrade. Legacy clients may incorrectly create data
    in the old format which would then need to be combined or otherwise
    reconciled with the data in v0.12 format. You might wish to take
    the opportunity to version-pin your installations so that future
    changes requiring controlled upgrades can be coordinated on a system
    wide basis.

