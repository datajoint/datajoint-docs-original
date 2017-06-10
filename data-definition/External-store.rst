External store
==============

.. important:: This section serves as the feature specification.  The implementation of this feature is schedule for the upcoming release.

DataJoint organizes most of its data in a relational database.  Relational databases excel at representing relationships between entities and storing structured data.
However, relational databases are not particularly well-suited for storing large continuous chunks of data such as images, signals, and movies.  
An attribute of type ``longblob`` can contain an object up to 4 GB in size (after compression) but storing many such large objects may hamper the performance of queries on the entire table.  A good rule of thumb is that objects  over 10 MB in size should not be put in the relational database.
In addition, storing data in cloud-hosted relational databases (e.g. AWS RDS) is more expensive than in cloud-hosted simple storage systems (e.g.  AWS S3). 

DataJoint introduces a new datatype, ``external`` to store large data objects within its relational framework.  

Defining an attribute of type ``external`` is done using the same :doc:`Definition-syntax` and, to the user, it works the same way as a ``blob`` attribute.  
However, its data are stored in an external storage system.  

Various systems can play the role of external storage: a shared file system accessible to all team members with access to these objects or a cloud storage solutions such as the AWS S3.  

For example, the following table  stores motion-aligned two-photon movies.

.. code-block:: text

    # Motion aligned movies
    -> twophoton.Scan
    ---
    aligned_movie :  external  # motion-aligned movie


All :doc:`../data-manipulation/Insert` and :doc:`../queries/Fetch` operations work identically for ``external`` attributes as for blob attributes with the same serialization protocol.  
Similar to blobs, external attributes cannot be used in restriction conditions.


Principles of operation
-----------------------
External storage is organized to emulate individual attribute values in the relational database.  
DataJoint organizes external storage to preserve the same data integrity principles in external storage as for relational storage.

1. An external storage location is specified in the DataJoint connection configuration.  This means that only one storage system can be used at a time.  This restriction may be resolved in the future along with the restriction of using one database server at a time.  At this point, DataJoint work with a single database server and a single external storage location at a time.

2. Each schema specifies a dedicated folder at the storage location.  No two schemas can share the same folder. The schema folder is specified in the schema object in MATLAB and Python.

3. Externally stored objects are identified by the `SHA-256 <https://en.wikipedia.org/wiki/SHA-2>`_ hash (in web-safe base-64 ASCII) of 

    a) the name of the table in which it is stored
    b) the primary key of the row in which it is stored
    c) the contents of the object after serialization but before compression

    This scheme ensures that even identical objects are individually stored in the external storage if they reside in different entries in the database.

4.  In the external storage, the objects are saved as files with the hash as the filename.

5. Each database schema has an auxiliary table named ``~external`` for representing externally stored objects.  

    It is automatically created the first time external storage is used.  The primary key of ``~external`` is the data hash. Other attributes are the status of the object (``stored``, ``deleted``), and the timestamp of the last event (creation or deletion).

    Below are sample entries in ``~external``.

    .. list-table:: ~external
       :widths: 15 15 15
       :header-rows: 1

       * - HASH
         - status
         - timestamp
       * - 1GEqtEU6JYEOLS4sZHeHDxWQ3JJfLlHVZio1ga25vd2
         - stored
         - 2017-06-07 23:14:01
       * - wqsKbNB1LKSX7aLEV+ACKWGr-XcB6+h6x91Wrfh9uf7
         - deleted
         - 2017-06-07 22:47:58

6. Attributes of type ``external`` are declared as renamed foreign keys referencing the ``~external`` table (but are not shown as such to the user).  

7. The :doc:`../data-manipulation/Insert` operation first saves all the external objects in the external storage, then inserts (or replaces) the corresponding tuples in ``~external`` with ``status="saved"``, and only then inserts the specified tuples.

8. The :doc:`../data-manipulation/Delete` operation first deletes the specified tuples, then updates the status of the item in ``~external`` to ``deleted`` and only then commits the transaction. The object is not actually deleted at this time.

9. The :doc:`../queries/Fetch` operations uses the hash value to find the data.  It need not access ``~external``.  If the cache folder is configured, then ``fetch`` operator retrieves the cached object without downloading it from external storage.  It also `touches` the file to update its creation date.

10.  Cleanup is performed regularly when the database is in light use or off-line.  Shallow cleanup removes all objects from external storage with ``status="deleted"`` in ``~external``.   Deep cleanup removes all objects from external storage with no entry in the ``~external`` table.

11. DataJoint never removes objects from the local cache folder.  The cache folder may just be periodically emptied entirely or based on file access date.  If dedicated cache folders are maintained for each schema, then a special procedure will be provided to remove all objects that are no longer listed in ``~/external``.

   Data removal from external storage is separated from the delete operations to ensure that data are not lost in race conditions between inserts and deletes of the same objects, especially in cases of transactional processing or in processes that are likely to get terminated.  The cleanup steps are performed in separate process when the risks of race conditions are minimal.  The process performing the cleanups must be isolated to prevent interruptions resulting in loss of data integrity. 

Configuration
-------------
The following steps must be performed to enable external storage:

1. Assign settings ``external-location``, ``external-account``, and ``external-token`` in DataJoint configuration.

  In Python this is performed using ``dj.config``.  

  In MATLAB, this is performed using ``dj.set``.

  ``external-location`` specifies the root path to the external data for all schemas as well as the protocol in the prefix such as ``file://`` or ``s3:``.

  ``exteral-account`` and ``external-token`` specify the credentials for accessing the external location.

2. For each schema, specify the name of the folder for that schema.

   In Python, this is  be done using the ``set_external_storage`` method of the schema object.

   In MATLAB, this is done using the ``setExternalStorge`` method of the schema object.

3. Optionally, for each schema specify the cache folder for local fetch cache. 

   In Python, this is done using the ``set_cache_folder`` method of the schema object.

   In MATLAB, this is done using the ``setCacheFolder`` method of the schema object.

