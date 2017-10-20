External store
==============

.. important:: This section serves as the feature specification.  The implementation of this feature is schedule for the upcoming release.

DataJoint organizes most of its data in a relational database.  
Relational databases excel at representing relationships between entities and storing structured data.
However, relational databases are not particularly well-suited for storing large continuous chunks of data such as images, signals, and movies.  
An attribute of type ``longblob`` can contain an object up to 4 GB in size (after compression) but storing many such large objects may hamper the performance of queries on the entire table.  
A good rule of thumb is that objects over 10 MB in size should not be put in the relational database.
In addition, storing data in cloud-hosted relational databases (e.g. AWS RDS) may be more expensive than in cloud-hosted simple storage systems (e.g.  AWS S3). 

DataJoint introduces a new datatype, ``external`` to store large data objects within its relational framework.  

Defining an attribute of type ``external`` is done using the same :doc:`Definition-syntax` and, to the user, it works the same way as a ``longblob`` attribute.  
However, its data are stored in an external storage system.  

Various systems can play the role of external storage: a shared file system accessible to all team members with access to these objects or a cloud storage solutions such as the AWS S3.  

For example, the following table stores motion-aligned two-photon movies.

.. code-block:: text

    # Motion aligned movies
    -> twophoton.Scan
    ---
    aligned_movie :  external  # motion-aligned movie


All :doc:`../data-manipulation/Insert` and :doc:`../queries/Fetch` operations work identically for ``external`` attributes as for blob attributes with the same serialization protocol.  
Similar to blobs, external attributes cannot be used in restriction conditions.

Multiple external storages may be configured and used simultaneously.  
In this case, the name of the external storage is specified in parentheses:

.. code-block:: text

    # Motion aligned movies
    -> twophoton.Scan
    ---
    aligned_movie :  external.preprocess  # motion-aligned movie


Principles of operation
-----------------------
External storage is organized to emulate individual attribute values in the relational database.  
DataJoint organizes external storage to preserve the same data integrity principles in external storage as for relational storage.

1. The external storage locations are specified in the DataJoint connection configuration, one for each storage. 

.. code-block:: python

   # default external storage
   dj.config['external'] = dict(
                 location='s3://microns-pipeline/analysis-store', 
                 account='vathes/chris-turner', 
                 token='LatVARch')
    
   # raw data storage 
   dj.config['extnernal.raw'] = dict(

   # preprocess external storage
   dj.config['external.preprocess'] = dict(
                 location='file://lab.ad.bcm.edu/store003') 


2. Each schema corresponds to a dedicated folder at the storage location with the same name as the database schema.   

3. Stored objects are identified by the `SHA-256 <https://en.wikipedia.org/wiki/SHA-2>`_ hash (in web-safe base-64 ASCII) of its serialized contents.  
   This scheme allows for the same object stored multiple times in the same schema to be stored only once. 

4. In the external storage, the objects are saved as files with the hash as the filename.

5. Each database schema has an auxiliary table named ``~external`` for representing externally stored objects.  

    It is automatically created the first time external storage is used.  The primary key of ``~external`` is the external storage name and the hash.  Other attributes are the ``count`` of references by tables in the schema, the ``size`` of the object in bytes, and the timestamp of the last event (creation, update, or deletion).

    Below are sample entries in ``~external``.

    .. list-table:: ~external
       :widths: 12 12 12 12 12
       :header-rows: 1

       * - STORAGE
         - HASH
         - count 
         - size
         - timestamp
       * - raw
         - 1GEqtEU6JYEOLS4sZHeHDxWQ3JJfLlHVZio1ga25vd2
         - 3
         - 1039536788
         - 2017-06-07 23:14:01
       * - 
         - wqsKbNB1LKSX7aLEV+ACKWGr-XcB6+h6x91Wrfh9uf7
         - 0
         - 168849430
         - 2017-06-07 22:47:58

6. Attributes of type ``external`` are declared as renamed foreign keys referencing the ``~external`` table (but are not shown as such to the user).  

7. The :doc:`../data-manipulation/Insert` operation first saves all the external objects in the external storage, then inserts the corresponding tuples in ``~external`` or, on duplicate, increments the ``count``, and only then inserts the specified tuples.

8. The :doc:`../data-manipulation/Delete` operation first deletes the specified tuples, then decrements the ``count`` of the item in ``~external`` and only then commits the entire transaction. The object is not actually deleted at this time.

9. The :doc:`../queries/Fetch` operation uses the hash values to find the data.  It need not access ``~external``.  If the cache folder is configured, then ``fetch`` operator retrieves the cached object without downloading it from external storage.  It does also ``touch`` the file to update its creation date to enable access recency check.

10.  Cleanup is performed regularly when the database is in light use or off-line.  Shallow cleanup removes all objects from external storage with ``count=0`` in ``~external``.   Deep cleanup removes all objects from external storage with no entry in the ``~external`` table.

11. DataJoint never removes objects from the local cache folder.  The cache folder may just be periodically emptied entirely or based on file access date.  If dedicated cache folders are maintained for each schema, then a special procedure will be provided to remove all objects that are no longer listed in ``~/external``.

   Data removal from external storage is separated from the delete operations to ensure that data are not lost in race conditions between inserts and deletes of the same objects, especially in cases of transactional processing or in processes that are likely to get terminated.  The cleanup steps are performed in separate process when the risks of race conditions are minimal.  The process performing the cleanups must be isolated to prevent interruptions resulting in loss of data integrity. 

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

