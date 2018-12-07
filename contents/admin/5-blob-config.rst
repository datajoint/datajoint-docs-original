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

DataJoint introduces a new datatype, ``external`` to store large data objects within its relational framework.

Defining an attribute of type ``external`` is done using the same :ref:`definition syntax <definitions>` and works the same way as a ``longblob`` attribute from the user's perspective.
However, its data are stored in an external storage system rather than in the relational database.

Various systems can play the role of external storage, including a shared file system accessible to all team members with access to these objects or a cloud storage solutions such as the AWS S3.

For example, the following table stores motion-aligned two-photon movies.

.. code-block:: text

    # Motion aligned movies
    -> twophoton.Scan
    ---
    aligned_movie :  external  # motion-aligned movie


All :ref:`insert <insert>` and :ref:`fetch <fetch>` operations work identically for ``external`` attributes as they do for blob attributes, with the same serialization protocol.
Similar to blobs, external attributes cannot be used in restriction conditions.

Multiple external storage configurations may be used simultaneously.
In this case, the specific external storage name is specified:

.. code-block:: text

    # Motion aligned movies
    -> twophoton.Scan
    ---
    aligned_movie :  external-raw  # motion-aligned movie


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

5. Each database schema has an auxiliary table named ``~external`` for representing externally stored objects.

   It is automatically created the first time external storage is used.
   The primary key of ``~external`` is the external storage name and the hash.
   Other attributes are the ``count`` of references by tables in the schema, the ``size`` of the object in bytes, and the timestamp of the last event (creation, update, or deletion).

   Below are sample entries in ``~external``.

   .. only:: latex

      .. list-table:: ~external
            :widths: 3 10 2 3 5 
            :header-rows: 1

            * - STORAGE
              - HASH
              - count
              - size
              - timestamp
            * - raw
              - 1GEqtEU6JYEOLS4sZHeHDxWQ3JJfLlH VZio1ga25vd2
              - 3
              - 1039536788
              - 2017-06-07 23:14:01
            * - 
              - wqsKbNB1LKSX7aLEV+ACKWGr-XcB6+h6x91Wrfh9uf7
              - 0
              - 168849430
              - 2017-06-07 22:47:58
   
   .. only:: html
    
        .. |br| unicode::  U+2028 .. line separator
            :trim:

        .. list-table:: ~external
            :widths: auto
            :header-rows: 1
            :align: center

            * - STORAGE
              - HASH
              - count
              - size
              - timestamp
            * - raw
              - 1GEqtEU6JYE |br| OLS4sZHeHDx |br| WQ3JJfLlHVZ |br| io1ga25vd2
              - 3
              - 1039536788
              - 2017-06-07 23:14:01
            * - 
              - wqsKbNB1LKS |br| X7aLEV+ACKW |br| Gr-XcB6+h6x |br| 91Wrfh9uf7
              - 0
              - 168849430
              - 2017-06-07 22:47:58
        
6. Attributes of type ``external`` are declared as renamed :ref:`foreign keys <dependencies>` referencing the ``~external`` table (but are not shown as such to the user).

7. The :ref:`insert <insert>` operation first saves all the external objects in the external storage, then inserts the corresponding entities in ``~external`` for new data or increments the ``count`` for duplicates.
   Only then are the specified entities inserted.

8. The :ref:`delete <delete>` operation first deletes the specified entities, then decrements the ``count`` of the item in ``~external``.
   Only then is the entire transaction committed, but the object is not actually deleted at this time.

9. The :ref:`fetch <fetch>` operation uses the hash values to find the data.
   In order to prevent excessive network overhead, a special external store named ``cache`` can be configured.
   If the ``cache`` is enabled, the ``fetch`` operation need not access ``~external`` directly.
   Instead ``fetch`` will retrieve the cached object without downloading directly from the 'real' external store.

10. Cleanup is performed regularly when the database is in light use or off-line.
    Shallow cleanup removes all objects from external storage with ``count=0`` in ``~external``.
    Deep cleanup removes all objects from external storage with no entry in the ``~external`` table.

11. DataJoint never removes objects from the local cache folder.
    The cache folder may just be periodically emptied entirely or based on file access date.
    If dedicated cache folders are maintained for each schema, then a special procedure will be provided to remove all objects that are no longer listed in ``~/external``.

Data removal from external storage is separated from the delete operations to ensure that data are not lost in race conditions between inserts and deletes of the same objects, especially in cases of transactional processing or in processes that are likely to get terminated.
The cleanup steps are performed in a separate process when the risks of race conditions are minimal.
The process performing the cleanups must be isolated to prevent interruptions resulting in loss of data integrity.

Configuration
-------------
The following steps must be performed to enable external storage:

1. Assign external location settings for each storage as shown in the Step 1 example above.

   In Python this is performed using ``dj.config``.

   In MATLAB, this is performed using ``dj.set``.

   ``location`` specifies the root path to the external data for all schemas as well as the protocol in the prefix such as ``file://`` or ``s3://``.

   ``account`` and ``token`` specify the credentials for accessing the external location.

2. Optionally, for each schema specify the cache folder for local fetch cache.

   In Python, this is done using the ``set_cache_folder`` method of the schema object.

   In MATLAB, this is done using the ``setCacheFolder`` method of the schema object.

Cleanup
-------

Deletion of records containing externally stored blobs is a 'soft delete' which only removes the database-side records from the database.
To remove the actual blob data, a separate cleanup process is run as described here.

1. Remove tracking entries for unused external blob items.

this will remove the tracking entry from the external storage table for any external blobs not referred to by any record.

.. include:: 5-blob-config_lang2.rst

1. Remove actual blob files from the desired external storage location.

.. important:: this action should only be performed if no modifications are being done to the tables using this external.

.. include:: 5-blob-config_lang3.rst

This will remove the actual unused files kept in the external storage 'external-name'.
